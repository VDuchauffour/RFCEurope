from CvPythonExtensions import *
from Core import (
    civilization,
    companies,
    civilizations,
    message,
    human,
    player,
    plot,
    show,
    team,
    text,
    turn,
    year,
    plots,
    cities,
)
from CoreTypes import (
    Building,
    City,
    Civ,
    Civic,
    Colony,
    Company,
    Project,
    ProvinceStatus,
    Region,
    Specialist,
    StabilityCategory,
    Religion,
    Improvement,
    Technology,
    Bonus,
    Wonder,
    Province,
)
from LocationsData import CITIES, CIV_CAPITAL_LOCATIONS, REGIONS
from PyUtils import rand
from RFCUtils import calculateDistance, countAchievedGoals, getNumberCargoShips, getMostAdvancedCiv
import UniquePowers
from StoredData import data
import random
from Events import handler
from Consts import MessageData

gc = CyGlobalContext()


tByzantiumControl = [
    Province.CALABRIA,
    Province.APULIA,
    Province.DALMATIA,
    Province.VERONA,
    Province.LOMBARDY,
    Province.LIGURIA,
    Province.TUSCANY,
    Province.LATIUM,
    Province.CORSICA,
    Province.SARDINIA,
    Province.SICILY,
    Province.TRIPOLITANIA,
    Province.IFRIQIYA,
]
tByzantiumControlII = [
    Province.COLONEA,
    Province.ANTIOCHIA,
    Province.CHARSIANON,
    Province.CILICIA,
    Province.ARMENIAKON,
    Province.ANATOLIKON,
    Province.PAPHLAGONIA,
    Province.THRAKESION,
    Province.OPSIKION,
    Province.CONSTANTINOPLE,
    Province.THRACE,
    Province.THESSALONIKI,
    Province.MOESIA,
    Province.MACEDONIA,
    Province.SERBIA,
    Province.ARBERIA,
    Province.EPIRUS,
    Province.THESSALY,
    Province.MOREA,
]
tFrankControl = [
    Province.SWABIA,
    Province.SAXONY,
    Province.LORRAINE,
    Province.ILE_DE_FRANCE,
    Province.NORMANDY,
    Province.PICARDY,
    Province.AQUITAINE,
    Province.PROVENCE,
    Province.BURGUNDY,
    Province.ORLEANS,
    Province.CHAMPAGNE,
    Province.CATALONIA,
    Province.LOMBARDY,
    Province.TUSCANY,
]
tArabiaControlI = [
    Province.ARABIA,
    Province.JERUSALEM,
    Province.SYRIA,
    Province.LEBANON,
    Province.ANTIOCHIA,
    Province.EGYPT,
    Province.CYRENAICA,
    Province.TRIPOLITANIA,
    Province.IFRIQIYA,
    Province.SICILY,
    Province.CRETE,
    Province.CYPRUS,
]
tArabiaControlII = [
    Province.ARABIA,
    Province.JERUSALEM,
    Province.SYRIA,
    Province.LEBANON,
    Province.ANTIOCHIA,
    Province.EGYPT,
]
tBulgariaControl = [
    Province.CONSTANTINOPLE,
    Province.THESSALONIKI,
    Province.SERBIA,
    Province.THRACE,
    Province.MACEDONIA,
    Province.MOESIA,
    Province.ARBERIA,
]
tCordobaWonders = [
    Wonder.ALHAMBRA,
    Wonder.LA_MEZQUITA,
    Wonder.GARDENS_AL_ANDALUS,
]
tCordobaIslamize = [
    Province.GALICIA,
    Province.CASTILE,
    Province.LEON,
    Province.LUSITANIA,
    Province.CATALONIA,
    Province.ARAGON,
    Province.NAVARRE,
    Province.VALENCIA,
    Province.LA_MANCHA,
    Province.ANDALUSIA,
]
tNorwayControl = [
    Province.THE_ISLES,
    Province.IRELAND,
    Province.SCOTLAND,
    Province.NORMANDY,
    Province.SICILY,
    Province.APULIA,
    Province.CALABRIA,
    Province.ICELAND,
]
tNorwayOutrank = [
    Civ.SWEDEN,
    Civ.DENMARK,
    Civ.SCOTLAND,
    Civ.ENGLAND,
    Civ.GERMANY,
    Civ.FRANCE,
]
# tNorseControl = [ Province.SICILY, Province.ICELAND, Province.NORTHUMBRIA, Province.SCOTLAND, Province.NORMANDY, Province.IRELAND, Province.NOVGOROD ]
tVenetianControl = [
    Province.EPIRUS,
    Province.DALMATIA,
    Province.VERONA,
    Province.ARBERIA,
]
tVenetianControlII = [
    Province.THESSALY,
    Province.MOREA,
    Province.CRETE,
    Province.CYPRUS,
]
tBurgundyControl = [
    Province.FLANDERS,
    Province.PICARDY,
    Province.PROVENCE,
    Province.BURGUNDY,
    Province.CHAMPAGNE,
    Province.LORRAINE,
]
tBurgundyOutrank = [Civ.FRANCE, Civ.ENGLAND, Civ.GERMANY]
tGermanyControl = [
    Province.TUSCANY,
    Province.LIGURIA,
    Province.LOMBARDY,
    Province.LORRAINE,
    Province.SWABIA,
    Province.SAXONY,
    Province.BAVARIA,
    Province.FRANCONIA,
    Province.BRANDENBURG,
    Province.HOLSTEIN,
]
tGermanyControlII = [
    Province.AUSTRIA,
    Province.FLANDERS,
    Province.POMERANIA,
    Province.SILESIA,
    Province.BOHEMIA,
    Province.MORAVIA,
    Province.SWABIA,
    Province.SAXONY,
    Province.BAVARIA,
    Province.FRANCONIA,
    Province.BRANDENBURG,
    Province.HOLSTEIN,
]
tKievControl = [
    Province.KIEV,
    Province.PODOLIA,
    Province.PEREYASLAVL,
    Province.SLOBODA,
    Province.CHERNIGOV,
    Province.VOLHYNIA,
    Province.MINSK,
    Province.POLOTSK,
    Province.SMOLENSK,
    Province.MOSCOW,
    Province.MUROM,
    Province.ROSTOV,
    Province.NOVGOROD,
    Province.VOLOGDA,
]
tHungaryControl = [
    Province.AUSTRIA,
    Province.CARINTHIA,
    Province.MORAVIA,
    Province.SILESIA,
    Province.BOHEMIA,
    Province.DALMATIA,
    Province.BOSNIA,
    Province.BANAT,
    Province.WALLACHIA,
    Province.MOLDOVA,
]
tHungaryControlII = [
    Province.THRACE,
    Province.MOESIA,
    Province.MACEDONIA,
    Province.THESSALONIKI,
    Province.WALLACHIA,
    Province.THESSALY,
    Province.MOREA,
    Province.EPIRUS,
    Province.ARBERIA,
    Province.SERBIA,
    Province.BANAT,
    Province.BOSNIA,
    Province.DALMATIA,
    Province.SLAVONIA,
]
tSpainConvert = [
    Province.GALICIA,
    Province.CASTILE,
    Province.LEON,
    Province.LUSITANIA,
    Province.CATALONIA,
    Province.ARAGON,
    Province.NAVARRE,
    Province.VALENCIA,
    Province.LA_MANCHA,
    Province.ANDALUSIA,
]
tPolishControl = [
    Province.BOHEMIA,
    Province.MORAVIA,
    Province.UPPER_HUNGARY,
    Province.PRUSSIA,
    Province.LITHUANIA,
    Province.LIVONIA,
    Province.POLOTSK,
    Province.MINSK,
    Province.VOLHYNIA,
    Province.PODOLIA,
    Province.MOLDOVA,
    Province.KIEV,
]
tGenoaControl = [
    Province.CORSICA,
    Province.SARDINIA,
    Province.CRETE,
    Province.RHODES,
    Province.THRAKESION,
    Province.CYPRUS,
    Province.CRIMEA,
]
tEnglandControl = [
    Province.AQUITAINE,
    Province.LONDON,
    Province.WALES,
    Province.WESSEX,
    Province.SCOTLAND,
    Province.EAST_ANGLIA,
    Province.MERCIA,
    Province.NORTHUMBRIA,
    Province.IRELAND,
    Province.NORMANDY,
    Province.BRETAGNE,
    Province.ILE_DE_FRANCE,
    Province.ORLEANS,
    Province.PICARDY,
]
tPortugalControlI = [Province.AZORES, Province.CANARIES, Province.MADEIRA]
tPortugalControlII = [Province.MOROCCO, Province.TETOUAN, Province.ORAN]
tAustriaControl = [
    Province.HUNGARY,
    Province.UPPER_HUNGARY,
    Province.AUSTRIA,
    Province.CARINTHIA,
    Province.BAVARIA,
    Province.TRANSYLVANIA,
    Province.PANNONIA,
    Province.MORAVIA,
    Province.SILESIA,
    Province.BOHEMIA,
]
tOttomanControlI = [
    Province.SERBIA,
    Province.BOSNIA,
    Province.BANAT,
    Province.MACEDONIA,
    Province.THRACE,
    Province.MOESIA,
    Province.CONSTANTINOPLE,
    Province.ARBERIA,
    Province.EPIRUS,
    Province.THESSALONIKI,
    Province.THESSALY,
    Province.MOREA,
    Province.COLONEA,
    Province.ANTIOCHIA,
    Province.CHARSIANON,
    Province.CILICIA,
    Province.ARMENIAKON,
    Province.ANATOLIKON,
    Province.PAPHLAGONIA,
    Province.THRAKESION,
    Province.OPSIKION,
    Province.SYRIA,
    Province.LEBANON,
    Province.JERUSALEM,
    Province.EGYPT,
]
tOttomanWonders = [
    Wonder.TOPKAPI_PALACE,
    Wonder.BLUE_MOSQUE,
    Wonder.SELIMIYE_MOSQUE,
    Wonder.TOMB_AL_WALID,
]
tOttomanControlII = [Province.AUSTRIA, Province.PANNONIA, Province.LESSER_POLAND]
tMoscowControl = [
    Province.DONETS,
    Province.KUBAN,
    Province.ZAPORIZHIA,
    Province.SLOBODA,
    Province.KIEV,
    Province.MOLDOVA,
    Province.CRIMEA,
    Province.PEREYASLAVL,
    Province.CHERNIGOV,
    Province.SIMBIRSK,
    Province.NIZHNYNOVGOROD,
    Province.VOLOGDA,
    Province.ROSTOV,
    Province.NOVGOROD,
    Province.KARELIA,
    Province.SMOLENSK,
    Province.POLOTSK,
    Province.MINSK,
    Province.VOLHYNIA,
    Province.PODOLIA,
    Province.MOSCOW,
    Province.MUROM,
]
# tSwedenControlI = [ Province.GOTALAND, Province.SVEALAND, Province.NORRLAND, Province.SKANELAND, Province.GOTLAND, Province.OSTERLAND ]
# tSwedenControlII = [ Province.SAXONY, Province.BRANDENBURG, Province.HOLSTEIN, Province.POMERANIA, Province.PRUSSIA, Province.GREATER_POLAND, Province.MASOVIA, Province.SUVALKIJA, Province.LITHUANIA, Province.LIVONIA, Province.ESTONIA, Province.SMOLENSK, Province.POLOTSK, Province.MINSK, Province.MUROM, Province.CHERNIGOV, Province.MOSCOW, Province.NOVGOROD, Province.ROSTOV ]
tSwedenControl = [Province.NORRLAND, Province.OSTERLAND, Province.KARELIA]
tNovgorodControl = [
    Province.NOVGOROD,
    Province.KARELIA,
    Province.ESTONIA,
    Province.LIVONIA,
    Province.ROSTOV,
    Province.VOLOGDA,
    Province.OSTERLAND,
]
# tNovgorodControlII = [ Province.KARELIA, Province.VOLOGDA ]
tMoroccoControl = [
    Province.MOROCCO,
    Province.MARRAKESH,
    Province.FEZ,
    Province.TETOUAN,
    Province.ORAN,
    Province.ALGIERS,
    Province.IFRIQIYA,
    Province.ANDALUSIA,
    Province.VALENCIA,
    Province.BALEARS,
]
tAragonControlI = [
    Province.CATALONIA,
    Province.VALENCIA,
    Province.BALEARS,
    Province.SICILY,
]
tAragonControlII = [
    Province.CATALONIA,
    Province.VALENCIA,
    Province.ARAGON,
    Province.BALEARS,
    Province.CORSICA,
    Province.SARDINIA,
    Province.SICILY,
    Province.CALABRIA,
    Province.APULIA,
    Province.PROVENCE,
    Province.THESSALY,
]
tPrussiaControlI = [
    Province.LITHUANIA,
    Province.SUVALKIJA,
    Province.LIVONIA,
    Province.ESTONIA,
    Province.POMERANIA,
    Province.PRUSSIA,
]
tPrussiaDefeat = [
    Civ.AUSTRIA,
    Civ.MOSCOW,
    Civ.GERMANY,
    Civ.SWEDEN,
    Civ.FRANCE,
    Civ.CASTILE,
]
tScotlandControl = [
    Province.SCOTLAND,
    Province.THE_ISLES,
    Province.IRELAND,
    Province.WALES,
    Province.BRETAGNE,
]
tDenmarkControlI = [
    Province.DENMARK,
    Province.SKANELAND,
    Province.GOTALAND,
    Province.SVEALAND,
    Province.MERCIA,
    Province.LONDON,
    Province.EAST_ANGLIA,
    Province.NORTHUMBRIA,
]
# tDenmarkControlII = [ Province.BRANDENBURG, Province.POMERANIA, Province.ESTONIA ]
tDenmarkControlIII = [
    Province.DENMARK,
    Province.NORWAY,
    Province.VESTFOLD,
    Province.SKANELAND,
    Province.GOTALAND,
    Province.SVEALAND,
    Province.NORRLAND,
    Province.GOTLAND,
    Province.OSTERLAND,
    Province.ESTONIA,
    Province.ICELAND,
]

# tHugeHungaryControl = ( 0, 23, 99, 72 )
totalLand = gc.getMap().getLandPlots()


@handler("GameStart")
def setup():
    # ignore AI goals
    bIgnoreAI = gc.getDefineINT("NO_AI_UHV_CHECKS") == 1
    data.bIgnoreAIUHV = bIgnoreAI
    if bIgnoreAI:
        for iPlayer in civilizations().majors().ids():
            if human() != iPlayer:
                setAllUHVFailed(iPlayer)


def setAllUHVFailed(iCiv):
    pPlayer = gc.getPlayer(iCiv)
    for i in range(3):
        pPlayer.setUHV(i, 0)


def isIgnoreAI():
    return data.bIgnoreAIUHV


@handler("cityBuilt")
def portugal_uhv_1(city):
    # Portugal UHV 1: Settle 3 cities on the Azores, Canaries and Madeira and 2 in Morocco, Tetouan and Oran
    iPlayer = city.getOwner()
    if iPlayer == Civ.PORTUGAL:
        if isPossibleUHV(iPlayer, 0, False):
            iProv = city.getProvince()
            if iProv in tPortugalControlI or iProv in tPortugalControlII:
                iCounter = player(Civ.PORTUGAL).getUHVCounter(0)
                iIslands = iCounter % 100
                iAfrica = iCounter / 100
                if iProv in tPortugalControlI:
                    iIslands += 1
                else:
                    iAfrica += 1
                if iIslands >= 3 and iAfrica >= 2:
                    wonUHV(Civ.PORTUGAL, 0)
                player(Civ.PORTUGAL).setUHVCounter(0, iAfrica * 100 + iIslands)


@handler("religionFounded")
def onReligionFounded(iReligion, iFounder):
    # Germany UHV 2: Start the Reformation (Found Protestantism)
    if iReligion == Religion.PROTESTANTISM:
        if iFounder == Civ.GERMANY:
            wonUHV(Civ.GERMANY, 1)
        else:
            lostUHV(Civ.GERMANY, 1)


@handler("cityAcquired")
def onCityAcquired(owner, iNewOwner, city, bConquest, bTrade):
    if not gc.getGame().isVictoryValid(7):  # Victory 7 == historical
        return

    iPlayer = owner
    iGameTurn = turn()

    # Bulgaria UHV 3: Do not lose a city to Barbarians, Mongols, Byzantines, or Ottomans before 1396
    if iPlayer == Civ.BULGARIA:
        if isPossibleUHV(iPlayer, 2, False):
            if iGameTurn <= year(1396):
                if iNewOwner in [Civ.BARBARIAN, Civ.BYZANTIUM, Civ.OTTOMAN]:
                    # conquered and flipped cities always count
                    # for traded cities, there should be a distinction between traded in peace (gift) and traded in ending a war (peace negotiations)
                    # instead of that, we check if the civ is at peace when the trade happens
                    # TODO#BUG# unfortunately the trade deal just ending a war is taken into account as a peace deal - maybe check if there was a war in this turn, or the last couple turns?
                    if not bTrade:
                        lostUHV(Civ.BULGARIA, 2)
                    else:
                        bIsAtWar = False
                        for civ in civilizations().take(Civ.BYZANTIUM, Civ.OTTOMAN).alive():
                            if civilization(Civ.BULGARIA).at_war(civ):
                                bIsAtWar = True
                        if bIsAtWar:
                            lostUHV(Civ.BULGARIA, 2)

    # Portugal UHV 2: Do not lose a city before 1640
    elif iPlayer == Civ.PORTUGAL:
        if isPossibleUHV(iPlayer, 1, False):
            # conquered and flipped cities always count
            # for traded cities, there should be a distinction between traded in peace (gift) and traded in ending a war (peace negotiations)
            # instead of that, we check if the civ is at peace when the trade happens
            # TODO#BUG# unfortunately the trade deal just ending a war is taken into account as a peace deal - maybe check if there was a war in this turn, or the last couple turns?
            if not bTrade:
                lostUHV(Civ.PORTUGAL, 1)
            else:
                bIsAtWar = False
                for civ in civilizations().majors().alive():
                    if civilization(Civ.BULGARIA).at_war(civ):
                        bIsAtWar = True
                        break
                if bIsAtWar:
                    lostUHV(Civ.PORTUGAL, 1)

    # Norway UHV 1: Going Viking
    elif iNewOwner == Civ.NORWAY and iGameTurn < year(1066) + 2:
        # Absinthe: city is already reduced by 1 on city conquest, so city.getPopulation() is one less than the original size (unless it was already 1)
        if bConquest:
            if city.getPopulation() > 1:
                player(Civ.NORWAY).setUHVCounter(
                    0, player(Civ.NORWAY).getUHVCounter(0) + city.getPopulation() + 1
                )
            else:
                player(Civ.NORWAY).setUHVCounter(
                    0, player(Civ.NORWAY).getUHVCounter(0) + city.getPopulation()
                )

    # Poland UHV 3: Construct 3 Catholic and Orthodox Cathedrals, 2 Protestant Cathedrals, and have at least 2 Jewish Quarters in your cities
    elif iNewOwner == Civ.POLAND:
        if isPossibleUHV(iNewOwner, 2, False):
            if city.hasBuilding(
                Wonder.KAZIMIERZ
            ):  # you cannot acquire religious buildings on conquest, only wonders
                iCounter = player(Civ.POLAND).getUHVCounter(2)
                iCathCath = (iCounter / 10000) % 10
                iOrthCath = (iCounter / 1000) % 10
                iProtCath = (iCounter / 100) % 10
                iJewishQu = 99
                iCounter = iJewishQu + 100 * iProtCath + 1000 * iOrthCath + 10000 * iCathCath
                player(Civ.POLAND).setUHVCounter(2, iCounter)
                if iCathCath >= 3 and iOrthCath >= 2 and iProtCath >= 2 and iJewishQu >= 2:
                    wonUHV(Civ.POLAND, 2)

    # Prussia UHV 2: Conquer two cities from each of Austria, Muscovy, Germany, Sweden, France and Spain between 1650 and 1763, if they are still alive
    elif iNewOwner == Civ.PRUSSIA:
        if isPossibleUHV(iNewOwner, 1, False):
            if owner in tPrussiaDefeat and year(1650) <= iGameTurn <= year(1763):
                lNumConq = []
                iConqRaw = player(Civ.PRUSSIA).getUHVCounter(1)
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
                    wonUHV(Civ.PRUSSIA, 1)

                iConqRaw = 0
                for iI in range(len(tPrussiaDefeat)):
                    iConqRaw += lNumConq[iI] * pow(10, iI)
                player(Civ.PRUSSIA).setUHVCounter(1, iConqRaw)


@handler("cityRazed")
def onCityRazed(city, iPlayer):
    # Sweden UHV 2: Raze 5 Catholic cities while being Protestant by 1660
    if iPlayer == Civ.SWEDEN:
        if isPossibleUHV(iPlayer, 1, False):
            if civilization(Civ.SWEDEN).has_state_religion(
                Religion.PROTESTANTISM
            ) and city.isHasReligion(Religion.CATHOLICISM):
                iRazed = player(Civ.SWEDEN).getUHVCounter(1) + 1
                player(Civ.SWEDEN).setUHVCounter(1, iRazed)
                if iRazed >= 5:
                    wonUHV(Civ.SWEDEN, 1)


@handler("unitPillage")
def onPillageImprovement(pUnit, iImprovement, iRoute, iOwner):
    # Norway UHV 1: Going Viking
    if pUnit.getOwner() == Civ.NORWAY and iRoute == -1 and turn() < year(1066) + 2:
        if plot(pUnit).getOwner() != Civ.NORWAY:
            player(Civ.NORWAY).setUHVCounter(0, player(Civ.NORWAY).getUHVCounter(0) + 1)


@handler("techAcquired")
def onTechAcquired(iTech, iTeam, iPlayer):
    if not gc.getGame().isVictoryValid(7):  # 7 == historical
        return

    # England UHV 3: Be the first to enter the Industrial age
    if iTech == Technology.INDUSTRIAL_TECH:
        if isPossibleUHV(Civ.ENGLAND, 2, False):
            if iPlayer == Civ.ENGLAND:
                wonUHV(Civ.ENGLAND, 2)
            else:
                lostUHV(Civ.ENGLAND, 2)


@handler("buildingBuilt")
def onBuildingBuilt(city, building_type):
    if not gc.getGame().isVictoryValid(7):  # 7 == historical
        return

    iPlayer = player(city)
    # Kiev UHV 1: Build 2 Orthodox cathedrals and 8 Orthodox monasteries by 1250
    if iPlayer == Civ.KIEV:
        if isPossibleUHV(iPlayer, 0, False):
            if building_type in [
                Building.ORTHODOX_MONASTERY,
                Building.ORTHODOX_CATHEDRAL,
            ]:
                iBuildSoFar = player(Civ.KIEV).getUHVCounter(0)
                iCathedralCounter = iBuildSoFar % 100
                iMonasteryCounter = iBuildSoFar / 100
                if building_type == Building.ORTHODOX_MONASTERY:
                    iMonasteryCounter += 1
                else:
                    iCathedralCounter += 1
                if iCathedralCounter >= 2 and iMonasteryCounter >= 8:
                    wonUHV(Civ.KIEV, 0)
                player(Civ.KIEV).setUHVCounter(0, 100 * iMonasteryCounter + iCathedralCounter)

    # Poland UHV 3: Construct 3 Catholic and Orthodox Cathedrals, 2 Protestant Cathedrals, and have at least 2 Jewish Quarters in your cities
    # HHG: Polish UHV3 now uses Wonder Kazimierz with maximum value 99, and all other buildings have boundary checks
    elif iPlayer == Civ.POLAND:
        if isPossibleUHV(iPlayer, 2, False):
            lBuildingList = [
                Building.CATHOLIC_CATHEDRAL,
                Building.ORTHODOX_CATHEDRAL,
                Building.PROTESTANT_CATHEDRAL,
                Building.JEWISH_QUARTER,
                Wonder.KAZIMIERZ,
            ]
            if building_type in lBuildingList:
                iCounter = player(Civ.POLAND).getUHVCounter(2)
                iCathCath = (iCounter / 10000) % 10
                iOrthCath = (iCounter / 1000) % 10
                iProtCath = (iCounter / 100) % 10
                iJewishQu = iCounter % 100
                if building_type == Building.CATHOLIC_CATHEDRAL and iCathCath < 9:
                    iCathCath += 1
                elif building_type == Building.ORTHODOX_CATHEDRAL and iOrthCath < 9:
                    iOrthCath += 1
                elif building_type == Building.PROTESTANT_CATHEDRAL and iProtCath < 9:
                    iProtCath += 1
                elif building_type == Wonder.KAZIMIERZ:
                    iJewishQu = 99
                elif building_type == Building.JEWISH_QUARTER and iJewishQu < 99:
                    iJewishQu += 1
                if iCathCath >= 3 and iOrthCath >= 3 and iProtCath >= 2 and iJewishQu >= 2:
                    wonUHV(Civ.POLAND, 2)
                iCounter = iJewishQu + 100 * iProtCath + 1000 * iOrthCath + 10000 * iCathCath
                player(Civ.POLAND).setUHVCounter(2, iCounter)

    # Cordoba UHV 2: Build the Alhambra, the Gardens of Al-Andalus, and La Mezquita by 1309
    if building_type in tCordobaWonders:
        if isPossibleUHV(Civ.CORDOBA, 1, False):
            if iPlayer == Civ.CORDOBA:
                iWondersBuilt = player(Civ.CORDOBA).getUHVCounter(1)
                player(Civ.CORDOBA).setUHVCounter(1, iWondersBuilt + 1)
                if iWondersBuilt == 2:  # so we already had 2 wonders, and this is the 3rd one
                    wonUHV(Civ.CORDOBA, 1)
            else:
                lostUHV(Civ.CORDOBA, 1)

    # Ottoman UHV 2: Construct the Topkapi Palace, the Blue Mosque, the Selimiye Mosque and the Tomb of Al-Walid by 1616
    if building_type in tOttomanWonders:
        if isPossibleUHV(Civ.OTTOMAN, 1, False):
            if iPlayer == Civ.OTTOMAN:
                iWondersBuilt = player(Civ.OTTOMAN).getUHVCounter(1)
                player(Civ.OTTOMAN).setUHVCounter(1, iWondersBuilt + 1)
                if iWondersBuilt == 3:  # so we already had 3 wonders, and this is the 4th one
                    wonUHV(Civ.OTTOMAN, 1)
            else:
                lostUHV(Civ.OTTOMAN, 1)


@handler("projectBuilt")
def onProjectBuilt(city, project):
    iPlayer = city.getOwner()
    bColony = isProjectAColony(project)
    # Absinthe: note that getProjectCount (thus getNumRealColonies too) won't count the latest project/colony
    # (which was currently built) if called from this function
    # way more straightforward, and also faster to use the UHVCounters for the UHV checks

    # Venice UHV 3: Be the first to build a Colony from the Age of Discovery (Vinland is from the Viking Age)
    if isPossibleUHV(Civ.VENECIA, 2, False):
        if project != Colony.VINLAND:
            if bColony:
                if iPlayer == Civ.VENECIA:
                    wonUHV(Civ.VENECIA, 2)
                else:
                    lostUHV(Civ.VENECIA, 2)

    # France UHV 3: Build 5 Colonies
    if iPlayer == Civ.FRANCE:
        if isPossibleUHV(iPlayer, 2, False):
            if bColony:
                player(Civ.FRANCE).setUHVCounter(2, player(Civ.FRANCE).getUHVCounter(2) + 1)
                if player(Civ.FRANCE).getUHVCounter(2) >= 5:
                    wonUHV(Civ.FRANCE, 2)

    # England UHV 2: Build 7 Colonies
    elif iPlayer == Civ.ENGLAND:
        if isPossibleUHV(iPlayer, 1, False):
            if bColony:
                player(Civ.ENGLAND).setUHVCounter(1, player(Civ.ENGLAND).getUHVCounter(1) + 1)
                if player(Civ.ENGLAND).getUHVCounter(1) >= 7:
                    wonUHV(Civ.ENGLAND, 1)

    # Spain UHV 2: Have more Colonies than any other nation in 1588 (while having at least 3)
    # this is only for the Main Screen counter
    elif iPlayer == Civ.CASTILE:
        player(Civ.CASTILE).setUHVCounter(1, player(Civ.CASTILE).getUHVCounter(1) + 1)

    # Portugal UHV 3: Build 5 Colonies
    elif iPlayer == Civ.PORTUGAL:
        if isPossibleUHV(iPlayer, 2, False):
            if bColony:
                player(Civ.PORTUGAL).setUHVCounter(2, player(Civ.PORTUGAL).getUHVCounter(2) + 1)
                if player(Civ.PORTUGAL).getUHVCounter(2) >= 5:
                    wonUHV(Civ.PORTUGAL, 2)

    # Dutch UHV 2: Build 3 Colonies and complete both Trading Companies
    elif iPlayer == Civ.DUTCH:
        if isPossibleUHV(iPlayer, 1, False):
            if bColony:
                player(Civ.DUTCH).setUHVCounter(1, player(Civ.DUTCH).getUHVCounter(1) + 1)
            if player(Civ.DUTCH).getUHVCounter(1) >= 3:
                iWestCompany = team(Civ.DUTCH).getProjectCount(Project.WEST_INDIA_COMPANY)
                iEastCompany = team(Civ.DUTCH).getProjectCount(Project.EAST_INDIA_COMPANY)
                # if the companies are already built previously, or currently being built (one of them is the current project)
                if project == Project.WEST_INDIA_COMPANY or iWestCompany >= 1:
                    if project == Project.EAST_INDIA_COMPANY or iEastCompany >= 1:
                        wonUHV(Civ.DUTCH, 1)

    # Denmark UHV 3: Build 3 Colonies and complete both Trading Companies
    elif iPlayer == Civ.DENMARK:
        if isPossibleUHV(iPlayer, 2, False):
            if bColony:
                player(Civ.DENMARK).setUHVCounter(2, player(Civ.DENMARK).getUHVCounter(2) + 1)
            if player(Civ.DENMARK).getUHVCounter(2) >= 3:
                iWestCompany = team(Civ.DENMARK).getProjectCount(Project.WEST_INDIA_COMPANY)
                iEastCompany = team(Civ.DENMARK).getProjectCount(Project.EAST_INDIA_COMPANY)
                # if the companies are already built previously, or currently being built (one of them is the current project)
                if project == Project.WEST_INDIA_COMPANY or iWestCompany == 1:
                    if project == Project.EAST_INDIA_COMPANY or iEastCompany == 1:
                        wonUHV(Civ.DENMARK, 2)


def getOwnedLuxes(pPlayer):
    lBonus = [
        Bonus.SHEEP,
        Bonus.DYE,
        Bonus.FUR,
        Bonus.GEMS,
        Bonus.GOLD,
        Bonus.INCENSE,
        Bonus.IVORY,
        Bonus.SILK,
        Bonus.SILVER,
        Bonus.SPICES,
        Bonus.WINE,
        Bonus.HONEY,
        Bonus.WHALE,
        Bonus.AMBER,
        Bonus.COTTON,
        Bonus.COFFEE,
        Bonus.TEA,
        Bonus.TOBACCO,
    ]
    iCount = 0
    for iBonus in lBonus:
        iCount += pPlayer.countOwnedBonuses(iBonus)
    return iCount


def getOwnedGrain(pPlayer):
    iCount = 0
    iCount += pPlayer.countOwnedBonuses(Bonus.WHEAT)
    iCount += pPlayer.countOwnedBonuses(Bonus.BARLEY)
    return iCount


def isProjectAColony(iProject):
    if iProject >= len(Project):
        return True
    else:
        return False


def getNumRealColonies(iPlayer):
    pPlayer = gc.getPlayer(iPlayer)
    tPlayer = gc.getTeam(pPlayer.getTeam())
    iCount = 0
    for col in Colony:
        if tPlayer.getProjectCount(col) > 0:
            iCount += 1
    return iCount


def getTerritoryPercentEurope(iPlayer, bReturnTotal=False):
    iTotal = 0
    iCount = 0
    for plot in plots.all().land().not_provinces(*REGIONS[Region.NOT_EUROPE]).entities():
        iTotal += 1
        if plot.getOwner() == iPlayer:
            iCount += 1
    if bReturnTotal:
        return iCount, iTotal
    return iCount


def checkByzantium(iGameTurn):

    # UHV 1: Own at least 6 cities in Calabria, Apulia, Dalmatia, Verona, Lombardy, Liguria, Tuscany, Latium, Corsica, Sardinia, Sicily, Tripolitania and Ifriqiya provinces in 632
    if iGameTurn == year(632):
        if isPossibleUHV(Civ.BYZANTIUM, 0, True):
            iNumCities = 0
            for iProv in tByzantiumControl:
                iNumCities += player(Civ.BYZANTIUM).getProvinceCityCount(iProv)
            if iNumCities >= 6:
                wonUHV(Civ.BYZANTIUM, 0)
            else:
                lostUHV(Civ.BYZANTIUM, 0)

    # UHV 2: Control Constantinople, Thrace, Thessaloniki, Moesia, Macedonia, Serbia, Arberia, Epirus, Thessaly, Morea, Colonea, Antiochia, Charsianon, Cilicia, Armeniakon, Anatolikon, Paphlagonia, Thrakesion and Opsikion in 1282
    elif iGameTurn == year(1282):
        if isPossibleUHV(Civ.BYZANTIUM, 1, True):
            if checkProvincesStates(Civ.BYZANTIUM, tByzantiumControlII):
                wonUHV(Civ.BYZANTIUM, 1)
            else:
                lostUHV(Civ.BYZANTIUM, 1)

    # UHV 3: Make Constantinople the largest and most cultured city while being the richest empire in the world in 1453
    elif iGameTurn == year(1453):
        if isPossibleUHV(Civ.BYZANTIUM, 2, True):
            x, y = CIV_CAPITAL_LOCATIONS[Civ.BYZANTIUM]
            iGold = player(Civ.BYZANTIUM).getGold()
            bMost = True
            for iCiv in civilizations().majors().ids():
                if iCiv != Civ.BYZANTIUM and gc.getPlayer(iCiv).isAlive():
                    if gc.getPlayer(iCiv).getGold() > iGold:
                        bMost = False
                        break
            if (
                gc.isLargestCity(x, y)
                and gc.isTopCultureCity(x, y)
                and gc.getMap().plot(x, y).getPlotCity().getOwner() == Civ.BYZANTIUM
                and bMost
            ):
                wonUHV(Civ.BYZANTIUM, 2)
            else:
                lostUHV(Civ.BYZANTIUM, 2)


def checkFrankia(iGameTurn):

    # UHV 1: Achieve Charlemagne's Empire by 840
    if isPossibleUHV(Civ.FRANCE, 0, True):
        if checkProvincesStates(Civ.FRANCE, tFrankControl):
            wonUHV(Civ.FRANCE, 0)
    if iGameTurn == year(840):
        expireUHV(Civ.FRANCE, 0)

    # UHV 2: Control Jerusalem in 1291
    elif iGameTurn == year(1291):
        if isPossibleUHV(Civ.FRANCE, 1, True):
            pJPlot = gc.getMap().plot(*CITIES[City.JERUSALEM])
            if pJPlot.isCity():
                if pJPlot.getPlotCity().getOwner() == Civ.FRANCE:
                    wonUHV(Civ.FRANCE, 1)
                else:
                    lostUHV(Civ.FRANCE, 1)
            else:
                lostUHV(Civ.FRANCE, 1)

    # UHV 3: Build 5 Colonies
    # handled in the onProjectBuilt function


def checkArabia(iGameTurn):

    # UHV 1: Control all territories from Tunisia to Asia Minor in 850
    if iGameTurn == year(850):
        if isPossibleUHV(Civ.ARABIA, 0, True):
            if checkProvincesStates(Civ.ARABIA, tArabiaControlI):
                wonUHV(Civ.ARABIA, 0)
            else:
                lostUHV(Civ.ARABIA, 0)

    # UHV 2: Control the Levant and Egypt in 1291AD while being the most advanced civilization
    elif iGameTurn == year(1291):
        if isPossibleUHV(Civ.ARABIA, 1, True):
            iMostAdvancedCiv = getMostAdvancedCiv()
            if (
                checkProvincesStates(Civ.ARABIA, tArabiaControlII)
                and iMostAdvancedCiv == Civ.ARABIA
            ):
                wonUHV(Civ.ARABIA, 1)
            else:
                lostUHV(Civ.ARABIA, 1)

    # UHV 3: Spread Islam to at least 35% of the population of Europe
    if isPossibleUHV(Civ.ARABIA, 2, True):
        iPerc = gc.getGame().calculateReligionPercent(Religion.ISLAM)
        if iPerc >= 35:
            wonUHV(Civ.ARABIA, 2)


def checkBulgaria(iGameTurn):

    # UHV 1: Conquer Moesia, Thrace, Macedonia, Serbia, Arberia, Thessaloniki and Constantinople by 917
    if isPossibleUHV(Civ.BULGARIA, 0, True):
        if checkProvincesStates(Civ.BULGARIA, tBulgariaControl):
            wonUHV(Civ.BULGARIA, 0)
    if iGameTurn == year(917):
        expireUHV(Civ.BULGARIA, 0)

    # UHV 2: Accumulate at least 100 Orthodox Faith Points by 1259
    if isPossibleUHV(Civ.BULGARIA, 1, True):
        if (
            civilization(Civ.BULGARIA).has_state_religion(Religion.ORTHODOXY)
            and player(Civ.BULGARIA).getFaith() >= 100
        ):
            wonUHV(Civ.BULGARIA, 1)
    if iGameTurn == year(1259):
        expireUHV(Civ.BULGARIA, 1)

    # UHV 3: Do not lose a city to Barbarians, Mongols, Byzantines, or Ottomans before 1396
    # Controlled in the onCityAcquired function
    elif iGameTurn == year(1396):
        if isPossibleUHV(Civ.BULGARIA, 2, True):
            wonUHV(Civ.BULGARIA, 2)


def checkCordoba(iGameTurn):

    # UHV 1: Make Cordoba the largest city in the world in 961
    if iGameTurn == year(961):
        if isPossibleUHV(Civ.CORDOBA, 0, True):
            x, y = CIV_CAPITAL_LOCATIONS[Civ.CORDOBA]
            if (
                gc.isLargestCity(x, y)
                and gc.getMap().plot(x, y).getPlotCity().getOwner() == Civ.CORDOBA
            ):
                wonUHV(Civ.CORDOBA, 0)
            else:
                lostUHV(Civ.CORDOBA, 0)

    # UHV 2: Build the Alhambra, the Gardens of Al-Andalus, and La Mezquita by 1309
    # Controlled in the onBuildingBuilt function
    elif iGameTurn == year(1309):
        expireUHV(Civ.CORDOBA, 1)

    # UHV 3: Make sure Islam is present in every city in the Iberian peninsula in 1492
    elif iGameTurn == year(1492):
        if isPossibleUHV(Civ.CORDOBA, 2, True):
            bIslamized = True
            for iProv in tCordobaIslamize:
                if not player(Civ.CORDOBA).provinceIsSpreadReligion(iProv, Religion.ISLAM):
                    bIslamized = False
                    break
            if bIslamized:
                wonUHV(Civ.CORDOBA, 2)
            else:
                lostUHV(Civ.CORDOBA, 2)


def checkNorway(iGameTurn):

    # Old UHV1: explore all water tiles
    # if ( iGameTurn == year(1009) and pNorway.getUHV( 0 ) == -1 ):
    # 	if ( gc.canSeeAllTerrain( iNorway, Terrain.OCEAN ) ):
    # 		wonUHV( iNorway, 0 )
    # 	else:
    # 		lostUHV( iNorway, 0 )

    # UHV 1: Gain 100 Viking Points and build Vinland by 1066
    # Viking points counted in the onCityAcquired, onPillageImprovement and onCombatResult functions
    if isPossibleUHV(Civ.NORWAY, 0, True):
        if (
            player(Civ.NORWAY).getUHVCounter(0) >= 100
            and team(Civ.NORWAY).getProjectCount(Colony.VINLAND) >= 1
        ):
            wonUHV(Civ.NORWAY, 0)
    if iGameTurn == year(1066):
        expireUHV(Civ.NORWAY, 0)

    # UHV 2: Conquer The Isles, Ireland, Scotland, Normandy, Sicily, Apulia, Calabria and Iceland by 1194
    if iGameTurn <= year(1194):
        if isPossibleUHV(Civ.NORWAY, 1, True):
            if checkProvincesStates(Civ.NORWAY, tNorwayControl):
                wonUHV(Civ.NORWAY, 1)
    if iGameTurn == year(1194):
        expireUHV(Civ.NORWAY, 1)

    # UHV 3: Have a higher score than Sweden, Denmark, Scotland, England, Germany and France in 1320
    elif iGameTurn == year(1320):
        if isPossibleUHV(Civ.NORWAY, 2, True):
            iNorwayRank = gc.getGame().getTeamRank(Civ.NORWAY)
            bIsOnTop = True
            for iTestPlayer in tNorwayOutrank:
                if gc.getGame().getTeamRank(iTestPlayer) < iNorwayRank:
                    bIsOnTop = False
                    break
            if bIsOnTop:
                wonUHV(Civ.NORWAY, 2)
            else:
                lostUHV(Civ.NORWAY, 2)


def checkDenmark(iGameTurn):

    # UHV 1: Control Denmark, Skaneland, G�taland, Svealand, Mercia, London, Northumbria and East Anglia in 1050
    if iGameTurn == year(1050):
        if isPossibleUHV(Civ.DENMARK, 0, True):
            if checkProvincesStates(Civ.DENMARK, tDenmarkControlI):
                wonUHV(Civ.DENMARK, 0)
            else:
                lostUHV(Civ.DENMARK, 0)

    # UHV 2: Control Denmark, Norway, Vestfold, Skaneland, G�taland, Svealand, Norrland, Gotland, �sterland, Estonia and Iceland in 1523
    elif iGameTurn == year(1523):
        if isPossibleUHV(Civ.DENMARK, 1, True):
            if checkProvincesStates(Civ.DENMARK, tDenmarkControlIII):
                wonUHV(Civ.DENMARK, 1)
            else:
                lostUHV(Civ.DENMARK, 1)

    # UHV 3: Build 3 Colonies and complete both Trading Companies
    # handled in the onProjectBuilt function


def checkVenecia(iGameTurn):

    # UHV 1: Conquer the Adriatic by 1004
    if isPossibleUHV(Civ.VENECIA, 0, True):
        if checkProvincesStates(Civ.VENECIA, tVenetianControl):
            wonUHV(Civ.VENECIA, 0)
    if iGameTurn == year(1004):
        expireUHV(Civ.VENECIA, 0)

    # UHV 2: Conquer Constantinople, Thessaly, Morea, Crete and Cyprus by 1204
    if isPossibleUHV(Civ.VENECIA, 1, True):
        if (
            player(Civ.VENECIA).getProvinceCurrentState(Province.CONSTANTINOPLE)
            >= ProvinceStatus.CONQUER
        ):
            if checkProvincesStates(Civ.VENECIA, tVenetianControlII):
                wonUHV(Civ.VENECIA, 1)
    if iGameTurn == year(1204):
        expireUHV(Civ.VENECIA, 1)

    # UHV 3: Be the first to build a Colony from the Age of Discovery
    # UHV 3: Vinland is from the Viking Age, all other Colonies are from the Age of Discovery
    # handled in the onProjectBuilt function


def checkBurgundy(iGameTurn):

    # UHV 1: Produce 12,000 culture points in your cities by 1336
    # The counter should be updated until the deadline for the challenge UHVs, even after UHV completion
    if iGameTurn < year(1336) + 2:
        iCulture = (
            player(Civ.BURGUNDY).getUHVCounter(0) + player(Civ.BURGUNDY).countCultureProduced()
        )
        player(Civ.BURGUNDY).setUHVCounter(0, iCulture)
        if isPossibleUHV(Civ.BURGUNDY, 0, True):
            if iCulture >= 12000:
                wonUHV(Civ.BURGUNDY, 0)
    if iGameTurn == year(1336):
        expireUHV(Civ.BURGUNDY, 0)

    # UHV 2: Control Burgundy, Provence, Picardy, Flanders, Champagne and Lorraine in 1376
    elif iGameTurn == year(1376):
        if isPossibleUHV(Civ.BURGUNDY, 1, True):
            if checkProvincesStates(Civ.BURGUNDY, tBurgundyControl):
                wonUHV(Civ.BURGUNDY, 1)
            else:
                lostUHV(Civ.BURGUNDY, 1)

    # UHV 3: Have a higher score than France, England and Germany in 1473
    elif iGameTurn == year(1473):
        if isPossibleUHV(Civ.BURGUNDY, 2, True):
            iBurgundyRank = gc.getGame().getTeamRank(Civ.BURGUNDY)
            bIsOnTop = True
            for iTestPlayer in tBurgundyOutrank:
                if gc.getGame().getTeamRank(iTestPlayer) < iBurgundyRank:
                    bIsOnTop = False
                    break
            if bIsOnTop:
                wonUHV(Civ.BURGUNDY, 2)
            else:
                lostUHV(Civ.BURGUNDY, 2)


def checkGermany(iGameTurn):

    # Old UHVs: Have most Catholic FPs in 1077 (Walk to Canossa)
    # 			Have 3 vassals

    # UHV 1: Control Lorraine, Swabia, Saxony, Bavaria, Franconia, Brandenburg, Holstein, Lombardy, Liguria and Tuscany in 1167
    if iGameTurn == year(1167):
        if isPossibleUHV(Civ.GERMANY, 0, True):
            if checkProvincesStates(Civ.GERMANY, tGermanyControl):
                wonUHV(Civ.GERMANY, 0)
            else:
                lostUHV(Civ.GERMANY, 0)

    # UHV 2: Start the Reformation (Found Protestantism)
    # Controlled in the onReligionFounded function

    # UHV 3: Control Swabia, Saxony, Bavaria, Franconia, Brandenburg, Holstein, Flanders, Pomerania, Silesia, Bohemia, Moravia and Austria in 1648
    elif iGameTurn == year(1648):
        if isPossibleUHV(Civ.GERMANY, 2, True):
            if checkProvincesStates(Civ.GERMANY, tGermanyControlII):
                wonUHV(Civ.GERMANY, 2)
            else:
                lostUHV(Civ.GERMANY, 2)


def checkNovgorod(iGameTurn):

    # UHV 1: Control Novgorod, Karelia, Estonia, Livonia, Rostov, Vologda and Osterland in 1284
    if iGameTurn == year(1284):
        if isPossibleUHV(Civ.NOVGOROD, 0, True):
            if checkProvincesStates(Civ.NOVGOROD, tNovgorodControl):
                wonUHV(Civ.NOVGOROD, 0)
            else:
                lostUHV(Civ.NOVGOROD, 0)

    # UHV 2: Control eleven sources of fur by 1397
    if isPossibleUHV(Civ.NOVGOROD, 1, True):
        if player(Civ.NOVGOROD).countCultBorderBonuses(Bonus.FUR) >= 11:
            wonUHV(Civ.NOVGOROD, 1)
    if iGameTurn == year(1397):
        expireUHV(Civ.NOVGOROD, 1)

    # UHV 3: Control the province of Moscow or have Muscovy as a vassal in 1478
    if iGameTurn == year(1478):
        if isPossibleUHV(Civ.NOVGOROD, 2, True):
            if (
                player(Civ.NOVGOROD).getProvinceCurrentState(Province.MOSCOW)
                >= ProvinceStatus.CONQUER
            ):
                wonUHV(Civ.NOVGOROD, 2)
            elif civilization(Civ.MOSCOW).is_alive() and civilization(Civ.MOSCOW).is_vassal(
                Civ.NOVGOROD
            ):
                wonUHV(Civ.NOVGOROD, 2)
            else:
                lostUHV(Civ.NOVGOROD, 2)


def checkKiev(iGameTurn):

    # UHV 1: Build 2 Orthodox cathedrals and 8 Orthodox monasteries by 1250
    # Controlled in the onBuildingBuilt function
    if iGameTurn == year(1250) + 1:
        expireUHV(Civ.KIEV, 0)

    # UHV 2: Control 10 provinces out of Kiev, Podolia, Pereyaslavl, Sloboda, Chernigov, Volhynia, Minsk, Polotsk, Smolensk, Moscow, Murom, Rostov, Novgorod and Vologda in 1288
    elif iGameTurn == year(1288):
        if isPossibleUHV(Civ.KIEV, 1, True):
            iConq = 0
            for iProv in tKievControl:
                if player(Civ.KIEV).getProvinceCurrentState(iProv) >= ProvinceStatus.CONQUER:
                    iConq += 1
            if iConq >= 10:
                wonUHV(Civ.KIEV, 1)
            else:
                lostUHV(Civ.KIEV, 1)

    # UHV 3: Produce 25000 food by 1300
    # The counter should be updated until the deadline for the challenge UHVs, even after UHV completion
    if iGameTurn < year(1300) + 2:
        iFood = player(Civ.KIEV).getUHVCounter(2) + player(Civ.KIEV).calculateTotalYield(
            YieldTypes.YIELD_FOOD
        )
        player(Civ.KIEV).setUHVCounter(2, iFood)
        if isPossibleUHV(Civ.KIEV, 2, True):
            if iFood > 25000:
                wonUHV(Civ.KIEV, 2)
    if iGameTurn == year(1300):
        expireUHV(Civ.KIEV, 2)


def checkHungary(iGameTurn):

    # UHV 1: Control Austria, Carinthia, Moravia, Silesia, Bohemia, Dalmatia, Bosnia, Banat, Wallachia and Moldova in 1490
    if iGameTurn == year(1490):
        if isPossibleUHV(Civ.HUNGARY, 0, True):
            if checkProvincesStates(Civ.HUNGARY, tHungaryControl):
                wonUHV(Civ.HUNGARY, 0)
            else:
                lostUHV(Civ.HUNGARY, 0)

    # UHV 2: Allow no Ottoman cities in Europe in 1541
    elif iGameTurn == year(1541):
        if isPossibleUHV(Civ.HUNGARY, 1, True):
            bClean = True
            if civilization(Civ.OTTOMAN).is_alive():
                for iProv in tHungaryControlII:
                    if player(Civ.OTTOMAN).getProvinceCityCount(iProv) > 0:
                        bClean = False
                        break
            if bClean:
                wonUHV(Civ.HUNGARY, 1)
            else:
                lostUHV(Civ.HUNGARY, 1)

    # UHV 3: Be the first to adopt Free Religion
    if isPossibleUHV(Civ.HUNGARY, 2, True):
        iReligiousCivic = player(Civ.HUNGARY).getCivics(4)
        if iReligiousCivic == Civic.FREE_RELIGION:
            wonUHV(Civ.HUNGARY, 2)
        else:
            for iPlayer in civilizations().majors().ids():
                pPlayer = gc.getPlayer(iPlayer)
                if pPlayer.isAlive() and pPlayer.getCivics(4) == Civic.FREE_RELIGION:
                    lostUHV(Civ.HUNGARY, 2)


def checkSpain(iGameTurn):

    # UHV 1: Reconquista (make sure Catholicism is the only religion present in every city in the Iberian peninsula in 1492)
    if iGameTurn == year(1492):
        if isPossibleUHV(Civ.CASTILE, 0, True):
            bConverted = True
            for iProv in tSpainConvert:
                if not player(Civ.CASTILE).provinceIsConvertReligion(iProv, Religion.CATHOLICISM):
                    bConverted = False
                    break
            if bConverted:
                wonUHV(Civ.CASTILE, 0)
            else:
                lostUHV(Civ.CASTILE, 0)

    # UHV 2: Have more Colonies than any other nation in 1588, while having at least 3
    elif iGameTurn == year(1588):
        if isPossibleUHV(Civ.CASTILE, 1, True):
            bMost = True
            iSpainColonies = getNumRealColonies(Civ.CASTILE)
            for iPlayer in civilizations().majors().ids():
                if iPlayer != Civ.CASTILE:
                    pPlayer = gc.getPlayer(iPlayer)
                    if pPlayer.isAlive() and getNumRealColonies(iPlayer) >= iSpainColonies:
                        bMost = False
            if bMost and iSpainColonies >= 3:
                wonUHV(Civ.CASTILE, 1)
            else:
                lostUHV(Civ.CASTILE, 1)

    # UHV 3: Ensure that Catholic nations have more population and more land than any other religion in 1648
    elif iGameTurn == year(1648):
        if isPossibleUHV(Civ.CASTILE, 2, True):
            if player(Civ.CASTILE).getStateReligion() != Religion.CATHOLICISM:
                lostUHV(Civ.CASTILE, 2)
            else:
                lLand = [0, 0, 0, 0, 0, 0]  # Prot, Islam, Cath, Orth, Jew, Pagan
                lPop = [0, 0, 0, 0, 0, 0]
                for iPlayer in civilizations().majors().ids():
                    pPlayer = gc.getPlayer(iPlayer)
                    iStateReligion = pPlayer.getStateReligion()
                    if iStateReligion > -1:
                        lLand[iStateReligion] += pPlayer.getTotalLand()
                        lPop[iStateReligion] += pPlayer.getTotalPopulation()
                    else:
                        lLand[5] += pPlayer.getTotalLand()
                        lPop[5] += pPlayer.getTotalPopulation()
                # The Barbarian civ counts as Pagan, Independent cities are included separately, based on the religion of the population
                lLand[5] += civilizations().barbarian().unwrap().player.getTotalLand()
                lPop[5] += civilizations().barbarian().unwrap().player.getTotalPopulation()
                for iIndyCiv in [
                    Civ.INDEPENDENT,
                    Civ.INDEPENDENT_2,
                    Civ.INDEPENDENT_3,
                    Civ.INDEPENDENT_4,
                ]:
                    for pCity in cities.owner(iIndyCiv).entities():
                        pIndyCiv = gc.getPlayer(iIndyCiv)
                        iAverageCityLand = pIndyCiv.getTotalLand() / pIndyCiv.getNumCities()
                        if pCity.getReligionCount() == 0:
                            lLand[5] += iAverageCityLand
                            lPop[5] += pCity.getPopulation()
                        else:
                            for iReligion in range(len(Religion)):
                                if pCity.isHasReligion(iReligion):
                                    lLand[iReligion] += iAverageCityLand / pCity.getReligionCount()
                                    lPop[iReligion] += (
                                        pCity.getPopulation() / pCity.getReligionCount()
                                    )

                iCathLand = lLand[Religion.CATHOLICISM]
                iCathPop = lPop[Religion.CATHOLICISM]

                bWon = True
                for iReligion in range(len(Religion) + 1):
                    if iReligion != Religion.CATHOLICISM:
                        if lLand[iReligion] >= iCathLand:
                            bWon = False
                            break
                        if lPop[iReligion] >= iCathPop:
                            bWon = False
                            break

                if bWon:
                    wonUHV(Civ.CASTILE, 2)
                else:
                    lostUHV(Civ.CASTILE, 2)


def checkScotland(iGameTurn):

    # UHV 1: Have 10 Forts and 4 Castles by 1296
    if isPossibleUHV(Civ.SCOTLAND, 0, True):
        iForts = player(Civ.SCOTLAND).getImprovementCount(Improvement.FORT)
        iCastles = player(Civ.SCOTLAND).countNumBuildings(Building.CASTLE)
        if iForts >= 10 and iCastles >= 4:
            wonUHV(Civ.SCOTLAND, 0)
    if iGameTurn == year(1296):
        expireUHV(Civ.SCOTLAND, 0)

    # UHV 2: Have 1500 Attitude Points with France by 1560 (Attitude Points are added every turn depending on your relations)
    if isPossibleUHV(Civ.SCOTLAND, 1, True):
        if civilization(Civ.FRANCE).is_alive():
            # Being at war with France gives a big penalty (and ignores most bonuses!)
            if civilization(Civ.SCOTLAND).at_war(Civ.FRANCE):
                iScore = -10
            else:
                # -1 for Furious 0 for Annoyed 1 for Cautious 2 for Pleased 3 for Friendly
                iScore = player(Civ.FRANCE).AI_getAttitude(Civ.SCOTLAND) - 1
                # Agreements
                if team(Civ.FRANCE).isOpenBorders(Civ.SCOTLAND):
                    iScore += 1
                if team(Civ.FRANCE).isDefensivePact(Civ.SCOTLAND):
                    iScore += 2
                # Imports/Exports
                iTrades = 0
                iTrades += player(Civ.SCOTLAND).getNumTradeBonusImports(Civ.FRANCE)
                iTrades += player(Civ.FRANCE).getNumTradeBonusImports(Civ.SCOTLAND)
                iScore += iTrades / 2
                # Common Wars
                for iEnemy in civilizations().majors().ids():
                    if iEnemy in [Civ.SCOTLAND, Civ.FRANCE]:
                        continue
                    if team(Civ.FRANCE).isAtWar(iEnemy) and team(Civ.SCOTLAND).isAtWar(iEnemy):
                        iScore += 2
            # Different religion from France also gives a penalty, same religion gives a bonus (but only if both have a state religion)
            if (
                civilization(Civ.SCOTLAND).has_a_state_religion()
                and civilization(Civ.FRANCE).has_a_state_religion()
            ):
                if (
                    civilization(Civ.SCOTLAND).state_religion()
                    != civilization(Civ.FRANCE).state_religion()
                ):
                    iScore -= 3
                elif (
                    civilization(Civ.SCOTLAND).state_religion()
                    == civilization(Civ.FRANCE).state_religion()
                ):
                    iScore += 1
            iOldScore = player(Civ.SCOTLAND).getUHVCounter(1)
            iNewScore = iOldScore + iScore
            player(Civ.SCOTLAND).setUHVCounter(1, iNewScore)
            if iNewScore >= 1500:
                wonUHV(Civ.SCOTLAND, 1)
    if iGameTurn == year(1560):
        expireUHV(Civ.SCOTLAND, 1)

    # UHV 3: Control Scotland, The Isles, Ireland, Wales, Brittany and Galicia in 1700
    elif iGameTurn == year(1700):
        if isPossibleUHV(Civ.SCOTLAND, 2, True):
            if checkProvincesStates(Civ.SCOTLAND, tScotlandControl):
                wonUHV(Civ.SCOTLAND, 2)
            else:
                lostUHV(Civ.SCOTLAND, 2)


def checkPoland(iGameTurn):

    # Old UHVs: Don't lose cities until 1772 or conquer Russia until 1772
    # 			Vassalize Russia, Germany and Austria

    # UHV 1: Food production between 1500 and 1520
    if year(1500) <= iGameTurn <= year(1520):
        if isPossibleUHV(Civ.POLAND, 0, True):
            iAgriculturePolish = player(Civ.POLAND).calculateTotalYield(YieldTypes.YIELD_FOOD)
            bFood = True
            for iPlayer in civilizations().majors().ids():
                if (
                    gc.getPlayer(iPlayer).calculateTotalYield(YieldTypes.YIELD_FOOD)
                    > iAgriculturePolish
                ):
                    bFood = False
                    break
            if bFood:
                wonUHV(Civ.POLAND, 0)
    if iGameTurn == year(1520) + 1:
        expireUHV(Civ.POLAND, 0)

    # UHV 2: Own at least 12 cities in the given provinces in 1569
    elif iGameTurn == year(1569):
        if isPossibleUHV(Civ.POLAND, 1, True):
            iNumCities = 0
            for iProv in tPolishControl:
                iNumCities += player(Civ.POLAND).getProvinceCityCount(iProv)
            if iNumCities >= 12:
                wonUHV(Civ.POLAND, 1)
            else:
                lostUHV(Civ.POLAND, 1)

    # UHV 3: Construct 3 Catholic and Orthodox Cathedrals, 2 Protestant Cathedrals, and have at least 2 Jewish Quarters in your cities
    # Controlled in the onBuildingBuilt and onCityAcquired functions


def checkGenoa(iGameTurn):

    # UHV 1: Control Corsica, Sardinia, Crete, Rhodes, Thrakesion, Cyprus and Crimea in 1400
    if iGameTurn == year(1400):
        if isPossibleUHV(Civ.GENOA, 0, True):
            if checkProvincesStates(Civ.GENOA, tGenoaControl):
                wonUHV(Civ.GENOA, 0)
            else:
                lostUHV(Civ.GENOA, 0)

    # UHV 2: Have the largest total amount of commerce from foreign Trade Route Exports and Imports in 1566
    # UHV 2: Export is based on your cities' trade routes with foreign cities, import is based on foreign cities' trade routes with your cities
    elif iGameTurn == year(1566):
        if isPossibleUHV(Civ.GENOA, 1, True):
            iGenoaTrade = player(Civ.GENOA).calculateTotalImports(
                YieldTypes.YIELD_COMMERCE
            ) + player(Civ.GENOA).calculateTotalExports(YieldTypes.YIELD_COMMERCE)
            bLargest = True
            for iPlayer in civilizations().majors().ids():
                if iPlayer != Civ.GENOA:
                    pPlayer = gc.getPlayer(iPlayer)
                    if (
                        pPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE)
                        + pPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE)
                        > iGenoaTrade
                    ):
                        bLargest = False
                        break
            if bLargest:
                wonUHV(Civ.GENOA, 1)
            else:
                lostUHV(Civ.GENOA, 1)

    # UHV 3: Have 8 Banks and own all Bank of St. George cities in 1625
    elif iGameTurn == year(1625):
        if isPossibleUHV(Civ.GENOA, 2, True):
            iBanks = 0
            for city in cities.owner(Civ.GENOA).entities():
                if (
                    city.getNumRealBuilding(Building.BANK) > 0
                    or city.getNumRealBuilding(Building.GENOA_BANK) > 0
                    or city.getNumRealBuilding(Building.ENGLISH_ROYAL_EXCHANGE) > 0
                ):
                    iBanks += 1
            iCompanyCities = player(Civ.GENOA).countCorporations(Company.ST_GEORGE)
            if iBanks >= 8 and iCompanyCities == companies[Company.ST_GEORGE].limit:
                wonUHV(Civ.GENOA, 2)
            else:
                lostUHV(Civ.GENOA, 2)


def checkMorocco(iGameTurn):

    # UHV 1: Control Morocco, Marrakesh, Fez, Tetouan, Oran, Algiers, Ifriqiya, Andalusia, Valencia and the Balearic Islands in 1248
    if iGameTurn == year(1248):
        if isPossibleUHV(Civ.MOROCCO, 0, True):
            if checkProvincesStates(Civ.MOROCCO, tMoroccoControl):
                wonUHV(Civ.MOROCCO, 0)
            else:
                lostUHV(Civ.MOROCCO, 0)

    # UHV 2: Have 5000 culture in each of three cities in 1465
    elif iGameTurn == year(1465):
        if isPossibleUHV(Civ.MOROCCO, 1, True):
            iGoodCities = 0
            for city in cities.owner(Civ.MOROCCO).entities():
                if city.getCulture(Civ.MOROCCO) >= 5000:
                    iGoodCities += 1
            if iGoodCities >= 3:
                wonUHV(Civ.MOROCCO, 1)
            else:
                lostUHV(Civ.MOROCCO, 1)

    # UHV 3: Destroy or vassalize Portugal, Spain, and Aragon by 1578
    if year(1164) <= iGameTurn <= year(1578):
        if isPossibleUHV(Civ.MOROCCO, 2, True):
            bConq = True
            if (
                (
                    civilization(Civ.CASTILE).is_alive()
                    and not civilization(Civ.CASTILE).is_vassal(Civ.MOROCCO)
                )
                or (
                    civilization(Civ.PORTUGAL).is_alive()
                    and not civilization(Civ.PORTUGAL).is_vassal(Civ.MOROCCO)
                )
                or (
                    civilization(Civ.ARAGON).is_alive()
                    and not civilization(Civ.ARAGON).is_vassal(Civ.MOROCCO)
                )
            ):
                bConq = False

            if bConq:
                wonUHV(Civ.MOROCCO, 2)
    if iGameTurn == year(1578) + 1:
        expireUHV(Civ.MOROCCO, 2)


def checkEngland(iGameTurn):

    # UHV 1: Control London, Wessex, East Anglia, Mercia, Northumbria, Scotland, Wales, Ireland, Normandy, Picardy, Bretagne, Il-de-France, Aquitania and Orleans in 1452
    if iGameTurn == year(1452):
        if isPossibleUHV(Civ.ENGLAND, 0, True):
            if checkProvincesStates(Civ.ENGLAND, tEnglandControl):
                wonUHV(Civ.ENGLAND, 0)
            else:
                lostUHV(Civ.ENGLAND, 0)

    # UHV 2: Build 7 Colonies
    # Controlled in the onProjectBuilt function

    # UHV 3: Be the first to enter the Industrial age
    # Controlled in the onTechAcquired function


def checkPortugal(iGameTurn):

    # UHV 1: Settle 3 cities on the Azores, Canaries and Madeira and 2 in Morocco, Tetouan and Oran
    # Controlled in the onCityBuilt function

    # UHV 2: Do not lose a city before 1640
    # Controlled in the onCityAcquired function
    if iGameTurn == year(1640):
        if isPossibleUHV(Civ.PORTUGAL, 1, True):
            wonUHV(Civ.PORTUGAL, 1)

    # UHV 3: Build 5 Colonies
    # Controlled in the onProjectBuilt function


def checkAragon(iGameTurn):

    # UHV 1: Control Catalonia, Valencia, Balears and Sicily in 1282
    if iGameTurn == year(1282):
        if isPossibleUHV(Civ.ARAGON, 0, True):
            if checkProvincesStates(Civ.ARAGON, tAragonControlI):
                wonUHV(Civ.ARAGON, 0)
            else:
                lostUHV(Civ.ARAGON, 0)

    # UHV 2: Have 12 Consulates of the Sea and 30 Trade Ships in 1444
    # UHV 2: Ships with at least one cargo space count as Trade Ships
    elif iGameTurn == year(1444):
        if isPossibleUHV(Civ.ARAGON, 1, True):
            iPorts = player(Civ.ARAGON).countNumBuildings(Building.ARAGON_SEAPORT)
            iCargoShips = getNumberCargoShips(Civ.ARAGON)
            if iPorts >= 12 and iCargoShips >= 30:
                wonUHV(Civ.ARAGON, 1)
            else:
                lostUHV(Civ.ARAGON, 1)

    # UHV 3: Control Catalonia, Valencia, Aragon, Balears, Corsica, Sardinia, Sicily, Calabria, Apulia, Provence and Thessaly in 1474
    elif iGameTurn == year(1474):
        if isPossibleUHV(Civ.ARAGON, 2, True):
            if checkProvincesStates(Civ.ARAGON, tAragonControlII):
                wonUHV(Civ.ARAGON, 2)
            else:
                lostUHV(Civ.ARAGON, 2)


def checkPrussia(iGameTurn):

    # UHV 1: Control Prussia, Suvalkija, Lithuania, Livonia, Estonia, and Pomerania in 1410
    if iGameTurn == year(1410):
        if isPossibleUHV(Civ.PRUSSIA, 0, True):
            if checkProvincesStates(Civ.PRUSSIA, tPrussiaControlI):
                wonUHV(Civ.PRUSSIA, 0)
            else:
                lostUHV(Civ.PRUSSIA, 0)

    # UHV 2: Conquer two cities from each of Austria, Muscovy, Germany, Sweden, France and Spain between 1650 and 1763, if they are still alive
    # Controlled in the onCityAcquired function
    if iGameTurn == year(1763) + 1:
        expireUHV(Civ.PRUSSIA, 1)

    # UHV 3: Settle a total of 15 Great People in your capital
    # UHV 3: Great People can be settled in any combination, Great Generals included
    if isPossibleUHV(Civ.PRUSSIA, 2, True):
        pCapital = player(Civ.PRUSSIA).getCapitalCity()
        iGPStart = gc.getInfoTypeForString("SPECIALIST_GREAT_PRIEST")
        iGPEnd = gc.getInfoTypeForString("SPECIALIST_GREAT_SPY")
        iGPeople = 0
        for iType in range(iGPStart, iGPEnd + 1):
            iGPeople += pCapital.getFreeSpecialistCount(iType)
        if iGPeople >= 15:
            wonUHV(Civ.PRUSSIA, 2)


def checkLithuania(iGameTurn):

    # UHV 1: Accumulate 2500 Culture points without declaring a state religion before 1386
    # The counter should be updated until the deadline for the challenge UHVs, even after UHV completion
    if iGameTurn < year(1386) + 2:
        iCulture = (
            player(Civ.LITHUANIA).getUHVCounter(0) + player(Civ.LITHUANIA).countCultureProduced()
        )
        player(Civ.LITHUANIA).setUHVCounter(0, iCulture)
        if isPossibleUHV(Civ.LITHUANIA, 0, True):
            if civilization(Civ.LITHUANIA).has_a_state_religion():
                lostUHV(Civ.LITHUANIA, 0)
            else:
                if iCulture >= 2500:
                    wonUHV(Civ.LITHUANIA, 0)
    if iGameTurn == year(1386):
        expireUHV(Civ.LITHUANIA, 0)

    # UHV 2: Control the most territory in Europe in 1430
    elif iGameTurn == year(1430):
        if isPossibleUHV(Civ.LITHUANIA, 1, True):
            bMost = True
            iCount = getTerritoryPercentEurope(Civ.LITHUANIA)
            for iOtherPlayer in civilizations().majors().ids():
                if not gc.getPlayer(iOtherPlayer).isAlive() or iOtherPlayer == Civ.LITHUANIA:
                    continue
                iOtherCount = getTerritoryPercentEurope(iOtherPlayer)
                if iOtherCount >= iCount:
                    bMost = False
                    break
            if bMost:
                wonUHV(Civ.LITHUANIA, 1)
            else:
                lostUHV(Civ.LITHUANIA, 1)

    # UHV 3: Destroy or Vassalize Muscovy, Novgorod and Prussia by 1795
    if year(1380) <= iGameTurn <= year(1795):
        if isPossibleUHV(Civ.LITHUANIA, 2, True):
            bConq = True
            if (
                (
                    civilization(Civ.MOSCOW).is_alive()
                    and not civilization(Civ.MOSCOW).is_vassal(Civ.LITHUANIA)
                )
                or (
                    civilization(Civ.NOVGOROD).is_alive()
                    and not civilization(Civ.NOVGOROD).is_vassal(Civ.LITHUANIA)
                )
                or (
                    civilization(Civ.PRUSSIA).is_alive()
                    and not civilization(Civ.PRUSSIA).is_vassal(Civ.LITHUANIA)
                )
            ):
                bConq = False

            if bConq:
                wonUHV(Civ.LITHUANIA, 2)
    if iGameTurn == year(1795) + 1:
        expireUHV(Civ.LITHUANIA, 2)


def checkAustria(iGameTurn):

    # UHV 1: Control all of medieval Austria, Hungary and Bohemia in 1617
    if iGameTurn == year(1617):
        if isPossibleUHV(Civ.AUSTRIA, 0, True):
            if checkProvincesStates(Civ.AUSTRIA, tAustriaControl):
                wonUHV(Civ.AUSTRIA, 0)
            else:
                lostUHV(Civ.AUSTRIA, 0)

    # UHV 2: Have 3 vassals in 1700
    elif iGameTurn == year(1700):
        if isPossibleUHV(Civ.AUSTRIA, 1, True):
            iCount = 0
            for iPlayer in civilizations().majors().ids():
                if iPlayer == Civ.AUSTRIA:
                    continue
                pPlayer = gc.getPlayer(iPlayer)
                if pPlayer.isAlive():
                    if gc.getTeam(pPlayer.getTeam()).isVassal(team(Civ.AUSTRIA).getID()):
                        iCount += 1
            if iCount >= 3:
                wonUHV(Civ.AUSTRIA, 1)
            else:
                lostUHV(Civ.AUSTRIA, 1)

    # UHV 3: Have the highest score in 1780
    elif iGameTurn == year(1780):
        if isPossibleUHV(Civ.AUSTRIA, 2, True):
            if gc.getGame().getTeamRank(Civ.AUSTRIA) == 0:
                wonUHV(Civ.AUSTRIA, 2)
            else:
                lostUHV(Civ.AUSTRIA, 2)


def checkTurkey(iGameTurn):

    # UHV 1: Control Constantinople, the Balkans, Anatolia, the Levant and Egypt in 1517
    if iGameTurn == year(1517):
        if isPossibleUHV(Civ.OTTOMAN, 0, True):
            if checkProvincesStates(Civ.OTTOMAN, tOttomanControlI):
                wonUHV(Civ.OTTOMAN, 0)
            else:
                lostUHV(Civ.OTTOMAN, 0)

    # UHV 2: Construct the Topkapi Palace, the Blue Mosque, the Selimiye Mosque and the Tomb of Al-Walid by 1616
    # Controlled in the onBuildingBuilt function
    elif iGameTurn == year(1616):
        expireUHV(Civ.OTTOMAN, 1)

    # UHV 3: Conquer Austria, Pannonia and Lesser Poland by 1683
    if isPossibleUHV(Civ.OTTOMAN, 2, True):
        if checkProvincesStates(Civ.OTTOMAN, tOttomanControlII):
            wonUHV(Civ.OTTOMAN, 2)
    if iGameTurn == year(1683):
        expireUHV(Civ.OTTOMAN, 2)


def checkMoscow(iGameTurn):

    # UHV 1: Free Eastern Europe from the Mongols (Make sure there are no Mongol (or any other Barbarian) cities in Russia and Ukraine in 1482)
    if iGameTurn == year(1482):
        if isPossibleUHV(Civ.MOSCOW, 0, True):
            bClean = True
            for iProv in tMoscowControl:
                if civilizations().barbarian().unwrap().player.getProvinceCityCount(iProv) > 0:
                    bClean = False
                    break
            if bClean:
                wonUHV(Civ.MOSCOW, 0)
            else:
                lostUHV(Civ.MOSCOW, 0)

    # UHV 2: Control at least 25% of Europe
    if isPossibleUHV(Civ.MOSCOW, 1, True):
        totalLand = gc.getMap().getLandPlots()
        RussianLand = player(Civ.MOSCOW).getTotalLand()
        if totalLand > 0:
            landPercent = (RussianLand * 100.0) / totalLand
        else:
            landPercent = 0.0
        if landPercent >= 25:
            wonUHV(Civ.MOSCOW, 1)

    # UHV 3: Get into warm waters (Conquer Constantinople or control an Atlantic Access resource)
    if isPossibleUHV(Civ.MOSCOW, 2, True):
        if player(Civ.MOSCOW).countCultBorderBonuses(Bonus.ACCESS) > 0:
            wonUHV(Civ.MOSCOW, 2)
        elif (
            gc.getMap().plot(*CIV_CAPITAL_LOCATIONS[Civ.BYZANTIUM]).getPlotCity().getOwner()
            == Civ.MOSCOW
        ):
            wonUHV(Civ.MOSCOW, 2)


def checkSweden(iGameTurn):

    # Old UHVs: Conquer Gotaland, Svealand, Norrland, Skaneland, Gotland and Osterland in 1600
    # 			Don't lose any cities to Poland, Lithuania or Russia before 1700
    # 			Have 15 cities in Saxony, Brandenburg, Holstein, Pomerania, Prussia, Greater Poland, Masovia, Suvalkija, Lithuania, Livonia, Estonia, Smolensk, Polotsk, Minsk, Murom, Chernigov, Moscow, Novgorod and Rostov in 1750

    # UHV 1: Have six cities in Norrland, Osterland and Karelia in 1323
    if iGameTurn == year(1323):
        if isPossibleUHV(Civ.SWEDEN, 0, True):
            iNumCities = 0
            for iProv in tSwedenControl:
                iNumCities += player(Civ.SWEDEN).getProvinceCityCount(iProv)
            if iNumCities >= 6:
                wonUHV(Civ.SWEDEN, 0)
            else:
                lostUHV(Civ.SWEDEN, 0)

    # UHV 2: Raze 5 Catholic cities while being Protestant by 1660
    # Controlled in the onCityRazed function
    elif iGameTurn == year(1660):
        expireUHV(Civ.SWEDEN, 1)

    # UHV 3: Control every coastal city on the Baltic Sea in 1750
    elif iGameTurn == year(1750):
        if isPossibleUHV(Civ.SWEDEN, 2, True):
            if UniquePowers.getNumForeignCitiesOnBaltic(Civ.SWEDEN, True) > 0:
                lostUHV(Civ.SWEDEN, 2)
            else:
                wonUHV(Civ.SWEDEN, 2)


def checkDutch(iGameTurn):

    # UHV 1: Settle 5 Great Merchants in Amsterdam by 1750
    if isPossibleUHV(Civ.DUTCH, 0, True):
        pPlot = gc.getMap().plot(*CIV_CAPITAL_LOCATIONS[Civ.DUTCH])
        if pPlot.isCity():
            city = pPlot.getPlotCity()
            if (
                city.getFreeSpecialistCount(Specialist.GREAT_MERCHANT) >= 5
                and city.getOwner() == Civ.DUTCH
            ):
                wonUHV(Civ.DUTCH, 0)
    if iGameTurn == year(1750):
        expireUHV(Civ.DUTCH, 0)

    # UHV 2: Build 3 Colonies and complete both Trading Companies
    # Controlled in the onProjectBuilt function

    # UHV 3: Become the richest country in Europe
    if isPossibleUHV(Civ.DUTCH, 2, True):
        iGold = player(Civ.DUTCH).getGold()
        bMost = True
        for iCiv in civilizations().majors().ids():
            if iCiv == Civ.DUTCH:
                continue
            pPlayer = gc.getPlayer(iCiv)
            if pPlayer.isAlive():
                if pPlayer.getGold() > iGold:
                    bMost = False
                    break
        if bMost:
            wonUHV(Civ.DUTCH, 2)


def checkProvincesStates(iPlayer, tProvinces):
    pPlayer = gc.getPlayer(iPlayer)
    for iProv in tProvinces:
        if pPlayer.getProvinceCurrentState(iProv) < ProvinceStatus.CONQUER:
            return False
    return True


def wonUHV(iCiv, iUHV):
    pCiv = gc.getPlayer(iCiv)
    pCiv.setUHV(iUHV, 1)
    pCiv.changeStabilityBase(StabilityCategory.EXPANSION, 3)
    if human() == iCiv:
        if iUHV == 0:
            sText = "first"
        elif iUHV == 1:
            sText = "second"
        elif iUHV == 2:
            sText = "third"
        show(text("TXT_KEY_VICTORY_UHV_GOAL_WON", sText))


def lostUHV(iCiv, iUHV):
    pCiv = gc.getPlayer(iCiv)
    pCiv.setUHV(iUHV, 0)
    if human() == iCiv:
        if iUHV == 0:
            sText = "first"
        elif iUHV == 1:
            sText = "second"
        elif iUHV == 2:
            sText = "third"
        show(text("TXT_KEY_VICTORY_UHV_GOAL_LOST", sText))


def switchUHV(iNewCiv, iOldCiv):
    pPlayer = gc.getPlayer(iNewCiv)
    for i in range(3):
        pPlayer.setUHV(i, -1)
    if isIgnoreAI():
        setAllUHVFailed(iOldCiv)


def isPossibleUHV(iCiv, iUHV, bAlreadyAIChecked):
    pCiv = gc.getPlayer(iCiv)
    if pCiv.getUHV(iUHV) != -1:
        return False
    if not pCiv.isAlive():
        return False

    if not bAlreadyAIChecked:
        if iCiv != human() and isIgnoreAI():  # Skip calculations if no AI UHV option is enabled
            return False

    return True


def expireUHV(iCiv, iUHV):
    # UHVs have to expire on the given deadline, even if the civ is not alive currently (would be an issue on respawns otherwise)
    # if isPossibleUHV(iCiv, iUHV, True):
    pCiv = gc.getPlayer(iCiv)
    if pCiv.getUHV(iUHV) == -1:
        lostUHV(iCiv, iUHV)


def set1200UHVDone(iCiv):
    if iCiv == Civ.BYZANTIUM:
        player(Civ.BYZANTIUM).setUHV(0, 1)
    elif iCiv == Civ.FRANCE:
        player(Civ.FRANCE).setUHV(0, 1)
    elif iCiv == Civ.ARABIA:
        player(Civ.ARABIA).setUHV(0, 1)
    elif iCiv == Civ.BULGARIA:
        player(Civ.BULGARIA).setUHV(0, 1)
    elif iCiv == Civ.VENECIA:  # Venice gets conquerors near Constantinople for 2nd UHV
        player(Civ.VENECIA).setUHV(0, 1)
    elif iCiv == Civ.GERMANY:
        player(Civ.GERMANY).setUHV(0, 1)
    elif iCiv == Civ.NORWAY:
        player(Civ.NORWAY).setUHV(0, 1)
    elif iCiv == Civ.DENMARK:
        player(Civ.DENMARK).setUHV(0, 1)
    elif iCiv == Civ.SCOTLAND:
        player(Civ.SCOTLAND).setUHVCounter(1, 100)


@handler("BeginPlayerTurn")
def checkPlayerTurn(iGameTurn, iPlayer):
    switchConditionsPerCiv = {
        Civ.BYZANTIUM: checkByzantium,
        Civ.FRANCE: checkFrankia,
        Civ.ARABIA: checkArabia,
        Civ.BULGARIA: checkBulgaria,
        Civ.CORDOBA: checkCordoba,
        Civ.VENECIA: checkVenecia,
        Civ.BURGUNDY: checkBurgundy,
        Civ.GERMANY: checkGermany,
        Civ.NOVGOROD: checkNovgorod,
        Civ.NORWAY: checkNorway,
        Civ.KIEV: checkKiev,
        Civ.HUNGARY: checkHungary,
        Civ.CASTILE: checkSpain,
        Civ.DENMARK: checkDenmark,
        Civ.SCOTLAND: checkScotland,
        Civ.POLAND: checkPoland,
        Civ.GENOA: checkGenoa,
        Civ.MOROCCO: checkMorocco,
        Civ.ENGLAND: checkEngland,
        Civ.PORTUGAL: checkPortugal,
        Civ.ARAGON: checkAragon,
        Civ.SWEDEN: checkSweden,
        Civ.PRUSSIA: checkPrussia,
        Civ.LITHUANIA: checkLithuania,
        Civ.AUSTRIA: checkAustria,
        Civ.OTTOMAN: checkTurkey,
        Civ.MOSCOW: checkMoscow,
        Civ.DUTCH: checkDutch,
    }

    pPlayer = gc.getPlayer(iPlayer)
    if iPlayer != human() and isIgnoreAI():
        return
    if not gc.getGame().isVictoryValid(7):  # 7 == historical
        return
    if not pPlayer.isAlive():
        return
    if iPlayer >= civilizations().main().len():
        return

    switchConditionsPerCiv[iPlayer](iGameTurn)

    # Generic checks:
    if not pPlayer.getUHV2of3():
        if (
            countAchievedGoals(iPlayer) >= 2
        ):  # in case the last 2 goals were achieved in the same turn
            # intermediate bonus
            pPlayer.setUHV2of3(True)
            if pPlayer.getNumCities() > 0:  # this check is needed, otherwise game crashes
                capital = pPlayer.getCapitalCity()
                # 3Miro: Golden Age after 2/3 victories
                capital.setHasRealBuilding(Building.TRIUMPHAL_ARCH, True)
                if pPlayer.isHuman():
                    message(
                        iPlayer, text("TXT_KEY_VICTORY_INTERMEDIATE"), color=MessageData.PURPLE
                    )
                    for iCiv in civilizations().majors().ids():
                        if iCiv != iPlayer:
                            pCiv = gc.getPlayer(iCiv)
                            if pCiv.isAlive():
                                iAttitude = pCiv.AI_getAttitude(iPlayer)
                                if iAttitude != 0:
                                    pCiv.AI_setAttitudeExtra(iPlayer, iAttitude - 1)

                    # Absinthe: maximum 3 of your rivals declare war on you
                    lCivs = [
                        iCiv
                        for iCiv in civilizations().main().ids()
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
                                iDistance = calculateDistance(
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
                                iRndnum = rand(7)
                                if iRndnum + iModifier > 6:
                                    teamCiv.declareWar(pPlayer.getTeam(), True, -1)
                                    iWarCounter += 1
                                    if iWarCounter == 3:
                                        break
                    if iWarCounter > 0:
                        message(
                            iPlayer,
                            text("TXT_KEY_VICTORY_RIVAL_CIVS"),
                            color=MessageData.LIGHT_RED,
                        )

    if gc.getGame().getWinner() == -1:
        if pPlayer.getUHV(0) == 1 and pPlayer.getUHV(1) == 1 and pPlayer.getUHV(2) == 1:
            gc.getGame().setWinner(iPlayer, 7)  # Historical Victory
