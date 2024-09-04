# Rhye's and Fall of Civilization: Europe - Barbarian units and cities

from CvPythonExtensions import *
from Consts import INDEPENDENT_CIVS, MessageData
from Core import (
    civilizations,
    message,
    event_popup,
    human,
    location,
    make_unit,
    make_units,
    text,
    turn,
    cities,
    plots,
)
from CoreTypes import Civ, Civic, Religion, Technology, Unit, Province
from Events import handler, popup_handler
from PyUtils import percentage, percentage_chance, rand, random_entry, choice
from RFCUtils import (
    cultureManager,
    flipCity,
    flipUnitsInCityAfter,
    flipUnitsInCitySecession,
    forcedInvasion,
    outerInvasion,
    outerSeaSpawn,
    squareSearch,
)
from TimelineData import DateTurn
from StoredData import data


gc = CyGlobalContext()


# Independent and barbarians city spawns
# Key: tCity = variations (coordinates, actual city name, chance), owner, population size, defender type, number of defenders, religion, workers
# Notes: Indy cities start with zero-sized culture, barbs with normal culture
# 		Added some initial food reserves on founding cities, so even independents won't shrink on their first turn anymore
# 		Barbarian cities start with 2 additional defender units
# 		Walls (and other buildings) can be added with the onCityBuilt function, in RiseAndFall.py
# 500 AD
tTangier = (
    [((27, 16), "Tangier", 100)],
    Civ.INDEPENDENT_2,
    1,
    Unit.CORDOBAN_BERBER,
    2,
    -1,
    0,
)
tBordeaux = ([((37, 38), "Burdigala", 100)], Civ.BARBARIAN, 2, Unit.ARCHER, 0, -1, 0)
tAlger = (
    [((40, 16), "Alger", 60), ((34, 13), "Tlemcen", 40)],
    Civ.INDEPENDENT_3,
    1,
    Unit.ARCHER,
    1,
    Religion.CATHOLICISM,
    0,
)
tBarcelona = (
    [((40, 28), "Barcino", 100)],
    Civ.INDEPENDENT_2,
    1,
    Unit.ARCHER,
    1,
    -1,
    0,
)
tToulouse = (
    [((41, 34), "Tolosa", 30), ((40, 34), "Tolosa", 30), ((42, 32), "Narbo", 40)],
    Civ.BARBARIAN,
    1,
    Unit.ARCHER,
    0,
    -1,
    0,
)
tMarseilles = (
    [((46, 32), "Massilia", 50), ((46, 33), "Aquae Sextiae", 50)],
    Civ.INDEPENDENT,
    1,
    Unit.ARCHER,
    1,
    Religion.CATHOLICISM,
    0,
)
tNantes = (
    [((36, 43), "Naoned", 50), ((35, 43), "Gwened", 30), ((37, 44), "Roazhon", 20)],
    Civ.INDEPENDENT_2,
    1,
    Unit.ARCHER,
    1,
    -1,
    0,
)
tCaen = (
    [((40, 47), "Caen", 100)],
    Civ.INDEPENDENT_4,
    2,
    Unit.ARCHER,
    1,
    Religion.CATHOLICISM,
    1,
)
tLyon = (
    [((46, 37), "Lyon", 100)],
    Civ.INDEPENDENT_3,
    2,
    Unit.ARCHER,
    2,
    Religion.CATHOLICISM,
    1,
)
tTunis = ([((49, 17), "Tunis", 100)], Civ.INDEPENDENT_4, 2, Unit.ARCHER, 1, -1, 0)
tYork = ([((39, 59), "Eboracum", 100)], Civ.INDEPENDENT_4, 1, Unit.ARCHER, 2, -1, 1)
tLondon = (
    [((41, 52), "Londinium", 100)],
    Civ.INDEPENDENT,
    2,
    Unit.ARCHER,
    2,
    Religion.CATHOLICISM,
    0,
)
tMilan = (
    [((52, 37), "Mediolanum", 100)],
    Civ.INDEPENDENT,
    2,
    Unit.ARCHER,
    2,
    Religion.CATHOLICISM,
    0,
)
tFlorence = (
    [((54, 32), "Florentia", 40), ((53, 32), "Pisae", 40), ((57, 31), "Ankon", 20)],
    Civ.INDEPENDENT_2,
    2,
    Unit.ARCHER,
    2,
    Religion.CATHOLICISM,
    0,
)
tTripoli = ([((54, 8), "Tripoli", 100)], Civ.BARBARIAN, 1, Unit.ARCHER, 1, -1, 0)
tAugsburg = (
    [((55, 41), "Augsburg", 100)],
    Civ.INDEPENDENT_3,
    1,
    Unit.ARCHER,
    2,
    -1,
    0,
)
tNapoli = (
    [((59, 24), "Neapolis", 40), ((60, 25), "Beneventum", 40), ((62, 24), "Tarentum", 20)],
    Civ.INDEPENDENT,
    2,
    Unit.ARCHER,
    1,
    -1,
    0,
)
tRagusa = (
    [((64, 28), "Ragusa", 100)],
    Civ.INDEPENDENT_2,
    1,
    Unit.ARCHER,
    2,
    Religion.CATHOLICISM,
    0,
)
tSeville = ([((27, 21), "Hispalis", 100)], Civ.INDEPENDENT_4, 1, Unit.ARCHER, 2, -1, 0)
tPalermo = (
    [((55, 19), "Palermo", 60), ((58, 17), "Syracuse", 40)],
    Civ.INDEPENDENT_3,
    2,
    Unit.ARCHER,
    1,
    Religion.CATHOLICISM,
    1,
)
# 552 AD
tInverness = (
    [((37, 67), "Inbhir Nis", 50), ((37, 65), "Scaig", 50)],
    Civ.BARBARIAN,
    1,
    Unit.ARCHER,
    1,
    -1,
    0,
)  # reduced to town on spawn of Scotland
# 600 AD
tRhodes = (
    [((80, 13), "Rhodes", 100)],
    Civ.INDEPENDENT_2,
    1,
    Unit.ARCHER,
    1,
    Religion.ORTHODOXY,
    0,
)
# 640 AD
tNorwich = (
    [((43, 55), "Norwich", 100)],
    Civ.INDEPENDENT_3,
    1,
    Unit.ARCHER,
    1,
    -1,
    1,
)  # reduced to town on spawn of England
# 670 AD
tKairouan = (
    [((48, 14), "Kairouan", 100)],
    Civ.INDEPENDENT_2,
    1,
    Unit.ARCHER,
    1,
    Religion.ISLAM,
    0,
)
# 680 AD
tToledo = (
    [((30, 27), "Toledo", 100)],
    Civ.BARBARIAN,
    1,
    Unit.ARCHER,
    1,
    Religion.CATHOLICISM,
    1,
)
tLeicester = (
    [((39, 56), "Ligeraceaster", 100)],
    Civ.INDEPENDENT,
    1,
    Unit.ARCHER,
    1,
    -1,
    0,
)  # reduced to town on spawn of England
# 700 AD
tValencia = (
    [((36, 25), "Valencia", 100)],
    Civ.INDEPENDENT,
    1,
    Unit.ARCHER,
    1,
    Religion.CATHOLICISM,
    1,
)
tPamplona = (
    [((35, 32), "Pamplona", 70), ((34, 33), "Pamplona", 30)],
    Civ.INDEPENDENT_4,
    1,
    Unit.CROSSBOWMAN,
    2,
    -1,
    0,
)
tLubeck = (
    [((57, 54), "Liubice", 40), ((57, 53), "Liubice", 60)],
    Civ.INDEPENDENT_2,
    1,
    Unit.ARCHER,
    2,
    -1,
    1,
)
tPorto = (
    [((23, 31), "Portucale", 100)],
    Civ.INDEPENDENT_3,
    1,
    Unit.CROSSBOWMAN,
    2,
    Religion.CATHOLICISM,
    0,
)
tDublin = (
    [((32, 58), "Teamhair", 100)],
    Civ.BARBARIAN,
    1,
    Unit.SPEARMAN,
    1,
    Religion.CATHOLICISM,
    1,
)  # Hill of Tara, later becomes Dublin
tDownpatrick = (
    [((33, 61), "Rath Celtair", 20), ((29, 60), "Cruiachain", 30), ((29, 56), "Caisel", 50)],
    Civ.BARBARIAN,
    1,
    Unit.ARCHER,
    0,
    -1,
    1,
)  # Cruiachain = Rathcroghan, later becomes Sligo; Caisel = Cashel, later becomes Cork
# 760 AD
tTonsberg = (
    [((57, 65), "Tonsberg", 100)],
    Civ.INDEPENDENT_3,
    1,
    Unit.ARCHER,
    2,
    -1,
    0,
)
# 768 AD
tRaska = ([((68, 28), "Ras", 100)], Civ.INDEPENDENT_2, 1, Unit.ARCHER, 2, -1, 1)
# 780 AD
tFez = ([((29, 12), "Fes", 100)], Civ.INDEPENDENT_4, 1, Unit.CROSSBOWMAN, 2, -1, 1)
# 800 AD
tMilanR = (
    [((52, 37), "Milano", 100)],
    Civ.INDEPENDENT,
    4,
    Unit.ARCHER,
    2,
    Religion.CATHOLICISM,
    0,
)  # respawn, in case it was razed
# tFlorenceR = ( [ ((54, 32), "Firenze", 100) ], Civ.INDEPENDENT_2, 4, Unit.ARCHER, 2, Religion.CATHOLICISM, 0 ) #respawn, doesn't work with the multiple options in 500AD
tPrague = (
    [((60, 44), "Praha", 100)],
    Civ.INDEPENDENT,
    1,
    Unit.CROSSBOWMAN,
    2,
    Religion.CATHOLICISM,
    1,
)
tKursk = ([((90, 48), "Kursk", 100)], Civ.INDEPENDENT_4, 1, Unit.ARCHER, 2, -1, 0)
tCalais = (
    [((44, 50), "Calais", 50), ((45, 50), "Dunkerque", 50)],
    Civ.INDEPENDENT_3,
    1,
    Unit.CROSSBOWMAN,
    2,
    -1,
    0,
)
tNidaros = (
    [((57, 71), "Nidaros", 100)],
    Civ.INDEPENDENT_3,
    1,
    Unit.ARCHER,
    1,
    -1,
    1,
)  # Trondheim
tUppsala = (
    [((65, 66), "Uppsala", 100)],
    Civ.INDEPENDENT_4,
    1,
    Unit.ARCHER,
    2,
    -1,
    1,
)  # reduced to town on spawn of Sweden
tBeloozero = (
    [((87, 65), "Beloozero", 100)],
    Civ.INDEPENDENT_4,
    1,
    Unit.CROSSBOWMAN,
    1,
    -1,
    1,
)
tZagreb = (
    [((62, 34), "Sisak", 100)],
    Civ.INDEPENDENT,
    2,
    Unit.ARCHER,
    2,
    -1,
    0,
)  # many Slavic princes reigned from Sisak in the 9th century, great for gameplay (buffer zone between Venice and Hungary)
# 850 AD
tBrennabor = (
    [((59, 50), "Brennabor", 50), ((60, 50), "Brennabor", 50)],
    Civ.BARBARIAN,
    1,
    Unit.ARCHER,
    2,
    -1,
    0,
)  # Brandenburg or Berlin
# 860 AD
# tEdinburgh = ( [ ((37, 63), "Eidyn Dun", 100) ], Civ.BARBARIAN, 1, Unit.ARCHER, 1, -1, 0)
# 880 AD
tApulum = (
    [((73, 35), "Belograd", 80), ((73, 37), "Napoca", 20)],
    Civ.INDEPENDENT,
    1,
    Unit.ARCHER,
    2,
    -1,
    0,
)  # Gyulafehérvár or Kolozsvár
# 900 AD
tTvanksta = (
    [((69, 53), "Tvanksta", 100)],
    Civ.INDEPENDENT_4,
    1,
    Unit.CROSSBOWMAN,
    2,
    -1,
    0,
)  # Königsberg
tKrakow = (
    [((68, 44), "Krakow", 100)],
    Civ.INDEPENDENT_3,
    1,
    Unit.CROSSBOWMAN,
    2,
    Religion.CATHOLICISM,
    0,
)
tRiga = (
    [((74, 58), "Riga", 100)],
    Civ.INDEPENDENT,
    2,
    Unit.CROSSBOWMAN,
    2,
    -1,
    1,
)  # maybe call it Duna in the early pediod (Duna is the name of a sheltered natural harbor near Riga)
tWales = (
    [((36, 54), "Caerdydd", 50), ((35, 57), "Aberffraw", 50)],
    Civ.BARBARIAN,
    1,
    Unit.ARCHER,
    1,
    -1,
    1,
)  # Cardiff and Caernarfon
tVisby = (
    [((67, 60), "Visby", 100)],
    Civ.INDEPENDENT_2,
    1,
    Unit.CROSSBOWMAN,
    1,
    -1,
    0,
)  # used to spawn in 1393 in the old system
# 911 AD
tCaenR = (
    [((40, 47), "Caen", 100)],
    Civ.INDEPENDENT_2,
    1,
    Unit.CROSSBOWMAN,
    2,
    Religion.CATHOLICISM,
    0,
)  # respawn, on the establishment of the Duchy of Normandy
# 960 AD
tMinsk = ([((79, 52), "Minsk", 100)], Civ.INDEPENDENT_3, 1, Unit.CROSSBOWMAN, 2, -1, 0)
tSmolensk = (
    [((84, 55), "Smolensk", 100)],
    Civ.INDEPENDENT_4,
    1,
    Unit.CROSSBOWMAN,
    1,
    -1,
    0,
)
# 988 AD
tDublinR = (
    [((32, 58), "Dubh Linn", 100)],
    Civ.BARBARIAN,
    1,
    Unit.CROSSBOWMAN,
    1,
    Religion.CATHOLICISM,
    1,
)  # respawn, on the traditional Irish foundation date of Dublin
# 1010 AD
tYaroslavl = (
    [((92, 61), "Yaroslavl", 100)],
    Civ.INDEPENDENT_3,
    1,
    Unit.CROSSBOWMAN,
    1,
    -1,
    0,
)
# 1050 AD
tGroningen = (
    [((52, 54), "Groningen", 100)],
    Civ.INDEPENDENT_2,
    1,
    Unit.CROSSBOWMAN,
    2,
    Religion.CATHOLICISM,
    0,
)
tKalmar = (
    [((64, 60), "Kalmar", 100)],
    Civ.INDEPENDENT_2,
    2,
    Unit.CROSSBOWMAN,
    1,
    Religion.CATHOLICISM,
    1,
)
# 1060 AD
# tMus = ( [ ((99, 21), "Mus", 100) ], Civ.BARBARIAN, 1, Unit.SELJUK_CROSSBOW, 2, -1, 0) #out of the map, not that important to represent the Seljuk/Timurid invasions this way
# 1110 AD
tGraz = (
    [((61, 37), "Graz", 100)],
    Civ.INDEPENDENT_3,
    2,
    Unit.CROSSBOWMAN,
    2,
    Religion.CATHOLICISM,
    0,
)
# 1124 AD
tHalych = (
    [((77, 41), "Halych", 100)],
    Civ.INDEPENDENT_2,
    2,
    Unit.CROSSBOWMAN,
    2,
    Religion.ORTHODOXY,
    0,
)
# 1200 AD
tRigaR = (
    [((74, 58), "Riga", 100)],
    Civ.INDEPENDENT,
    3,
    Unit.CROSSBOWMAN,
    2,
    -1,
    1,
)  # respawn
# tSaraiBatu = ( [ ((99, 40), "Sarai Batu", 100) ], Civ.BARBARIAN, 1, Unit.MONGOL_KESHIK, 2, -1, 0) #out of the map, not that important to represent the Mongol invasions this way
# 1227 AD
tTripoliR = (
    [((54, 8), "Tarabulus", 100)],
    Civ.BARBARIAN,
    3,
    Unit.ARBALEST,
    2,
    Religion.ISLAM,
    1,
)  # respawn
# 1250 AD
tAbo = ([((71, 66), "Abo", 100)], Civ.INDEPENDENT_4, 1, Unit.CROSSBOWMAN, 1, -1, 0)
tPerekop = (
    [((87, 36), "Or Qapi", 100)],
    Civ.BARBARIAN,
    1,
    Unit.MONGOL_KESHIK,
    2,
    -1,
    0,
)
# 1320 AD
tNizhnyNovgorod = (
    [((97, 58), "Nizhny Novgorod", 100)],
    Civ.INDEPENDENT,
    1,
    Unit.CROSSBOWMAN,
    1,
    -1,
    0,
)
# 1392 AD
tTanais = (
    [((96, 38), "Tana", 100)],
    Civ.BARBARIAN,
    1,
    Unit.LONGBOWMAN,
    2,
    Religion.ISLAM,
    0,
)
# 1410 AD
tReykjavik = (
    [((2, 70), "Reykjavik", 100)],
    Civ.INDEPENDENT,
    1,
    Unit.VIKING_BERSERKER,
    2,
    -1,
    0,
)
# 1530 AD
tValletta = (
    [((57, 14), "Valletta", 100)],
    Civ.INDEPENDENT_4,
    1,
    Unit.KNIGHT_OF_ST_JOHNS,
    3,
    Religion.CATHOLICISM,
    0,
)

dIndependentCities = {
    DateTurn.i500AD: [
        tTangier,
        tBordeaux,
        tAlger,
        tBarcelona,
        tToulouse,
        tMarseilles,
        tNantes,
        tCaen,
        tLyon,
        tTunis,
        tYork,
        tLondon,
        tMilan,
        tFlorence,
        tTripoli,
        tAugsburg,
        tRagusa,
        tSeville,
        tPalermo,
    ],
    DateTurn.i504AD: [tNapoli],
    DateTurn.i552AD: [tInverness],
    DateTurn.i600AD: [tRhodes],
    DateTurn.i640AD: [tNorwich],
    DateTurn.i670AD: [tKairouan],
    DateTurn.i680AD: [tToledo, tLeicester],
    DateTurn.i700AD: [tValencia, tPamplona, tLubeck, tPorto, tDublin, tDownpatrick],
    DateTurn.i760AD: [tTonsberg],
    DateTurn.i768AD: [tRaska],
    DateTurn.i780AD: [tFez],
    DateTurn.i800AD: [tMilanR, tPrague, tKursk, tCalais, tNidaros, tUppsala, tBeloozero, tZagreb],
    DateTurn.i850AD: [tBrennabor],
    DateTurn.i880AD: [tApulum],
    DateTurn.i900AD: [tTvanksta, tKrakow, tRiga, tWales, tVisby],
    DateTurn.i911AD: [tCaenR],
    DateTurn.i960AD: [tMinsk, tSmolensk],
    DateTurn.i988AD: [tDublinR],
    DateTurn.i1010AD: [tYaroslavl],
    DateTurn.i1050AD: [tGroningen, tKalmar],
    DateTurn.i1110AD: [tGraz],
    DateTurn.i1124AD: [tHalych],
    DateTurn.i1200AD: [tRigaR],
    DateTurn.i1227AD: [tTripoliR],
    DateTurn.i1250AD: [tAbo, tPerekop],
    DateTurn.i1320AD: [tNizhnyNovgorod],
    DateTurn.i1393AD: [tTanais],
    DateTurn.i1410AD: [tReykjavik],
    DateTurn.i1530AD: [tValletta],
}


# Minor Nations structure: [ int Province: all cities in this province will revolt
# 			list nations: a city controlled by those players will not revolt (i.e. Greece wouldn't revolt against the Byz)
# 			list religions: a city owned by someone with one of those state religions will not revolt (i.e. Jerusalem doesn't revolt against Muslims)
# 			list revolt dates: the dates for the revolt,
# 			list revolt strength: this is subtracted from the odds to suppress the revolt (i.e. high number more likely to succeed in the revolt)
# 			list units: corresponding to the revolt, if we crack down on the rebels, what barbarian units should spawn
# 			list number: corresponding to the revolt, if we crack down on the rebels, how many units should spawn (note if we don't bribe the Lords, then double the number of Units will spawn)
# 			list text keys: text keys for "The Nation" and "Nation Adjective"
# Note: lists 3, 4, 5, 6 should have the same size
# Note: you should increase the size of 'lNextMinorRevolt' in StoredData to be at least the number of minor nations
lMinorNations = [
    [
        Province.SERBIA,
        [],
        [],
        [DateTurn.i508AD, DateTurn.i852AD, DateTurn.i1346AD],
        [20, 20, 20],
        [Unit.AXEMAN, Unit.AXEMAN, Unit.LONG_SWORDSMAN],
        [2, 1, 2],
        ["TXT_KEY_THE_SERBS", "TXT_KEY_SERBIAN"],
    ],
    [
        Province.SCOTLAND,
        [Civ.SCOTLAND],
        [],
        [DateTurn.i1297AD, DateTurn.i1569AD, DateTurn.i1715AD],
        [20, 10, 20],
        [Unit.HIGHLANDER, Unit.MUSKETMAN, Unit.GRENADIER],
        [2, 2, 2],
        ["TXT_KEY_THE_SCOTS", "TXT_KEY_SCOTTISH"],
    ],
    [
        Province.CATALONIA,
        [Civ.ARAGON],
        [],
        [DateTurn.i1164AD + 10, DateTurn.i1640AD],
        [20, 10],
        [Unit.LONG_SWORDSMAN, Unit.MUSKETMAN],
        [2, 2],
        ["TXT_KEY_THE_CATALANS", "TXT_KEY_CATALAN"],
    ],
    [
        Province.JERUSALEM,
        [Civ.ARABIA, Civ.OTTOMAN, Civ.BYZANTIUM],
        [Religion.ISLAM],
        [
            DateTurn.i1099AD + 8,
            DateTurn.i1099AD + 16,
            DateTurn.i1099AD + 25,
            DateTurn.i1099AD + 33,
            DateTurn.i1099AD + 40,
            DateTurn.i1099AD + 47,
            DateTurn.i1099AD + 55,
            DateTurn.i1099AD + 65,
        ],
        [30, 30, 40, 40, 30, 30, 30, 30],
        [
            Unit.MACEMAN,
            Unit.MACEMAN,
            Unit.MACEMAN,
            Unit.KNIGHT,
            Unit.KNIGHT,
            Unit.KNIGHT,
            Unit.KNIGHT,
            Unit.KNIGHT,
        ],
        [3, 3, 4, 3, 3, 3, 3, 3],
        ["TXT_KEY_THE_MUSLIMS", "TXT_KEY_MUSLIM"],
    ],
    [
        Province.SYRIA,
        [Civ.ARABIA, Civ.OTTOMAN, Civ.BYZANTIUM],
        [Religion.ISLAM],
        [
            DateTurn.i1099AD + 8,
            DateTurn.i1099AD + 16,
            DateTurn.i1099AD + 25,
            DateTurn.i1099AD + 33,
            DateTurn.i1099AD + 40,
            DateTurn.i1099AD + 47,
            DateTurn.i1099AD + 55,
            DateTurn.i1099AD + 65,
        ],
        [30, 30, 40, 40, 30, 30, 30, 30],
        [
            Unit.MACEMAN,
            Unit.MACEMAN,
            Unit.MACEMAN,
            Unit.KNIGHT,
            Unit.KNIGHT,
            Unit.KNIGHT,
            Unit.KNIGHT,
            Unit.KNIGHT,
        ],
        [3, 3, 4, 3, 3, 3, 3, 3],
        ["TXT_KEY_THE_MUSLIMS", "TXT_KEY_MUSLIM"],
    ],
    [
        Province.ORAN,
        [],
        [],
        [DateTurn.i1236AD, DateTurn.i1346AD, DateTurn.i1359AD, DateTurn.i1542AD],
        [40, 10, 10, 20],
        [
            Unit.KNIGHT,
            Unit.HEAVY_LANCER,
            Unit.HEAVY_LANCER,
            Unit.MUSKETMAN,
        ],
        [2, 2, 2, 2],
        ["TXT_KEY_THE_ZIYYANIDS", "TXT_KEY_ZIYYANID"],
    ],
    [
        Province.FEZ,
        [Civ.MOROCCO],
        [],
        [DateTurn.i1473AD],
        [30],
        [Unit.ARQUEBUSIER],
        [4],
        ["TXT_KEY_THE_WATTASIDS", "TXT_KEY_WATTASID"],
    ],
]
# 3Miro: Jerusalem and Syria were added here, so the Crusaders will not be able to control it for too long


def getTempFlippingCity():
    return data.temp_flipping_city


def setTempFlippingCity(tNewValue):
    data.temp_flipping_city = tNewValue


@handler("BeginGameTurn")
def checkTurn(iGameTurn):
    # Handicap level modifier
    iHandicap = gc.getGame().getHandicapType() - 1
    # gc.getGame().getHandicapType: Viceroy=0, Monarch=1, Emperor=2
    # iHandicap: Viceroy=-1, Monarch=0, Emperor=1

    # The Human player usually gets some additional barbarians
    iHuman = human()

    # Mediterranean Pirates (Light before 1500, then heavy for rest of game)
    if DateTurn.i960AD <= iGameTurn < DateTurn.i1401AD:
        spawnPirate(
            Civ.BARBARIAN,
            (9, 15),
            (55, 33),
            Unit.WAR_GALLEY,
            2,
            0,
            0,
            iGameTurn,
            10,
            3,
            outerSeaSpawn,
        )
    elif iGameTurn >= DateTurn.i1401AD:
        spawnPirate(
            Civ.BARBARIAN,
            (9, 15),
            (55, 33),
            Unit.CORSAIR,
            2,
            0,
            0,
            iGameTurn,
            10,
            3,
            outerSeaSpawn,
            text("TXT_KEY_BARBARIAN_NAMES_BARBARY_PIRATES"),
        )
        # extra Corsairs around Tunisia
        spawnPirate(
            Civ.BARBARIAN,
            (42, 15),
            (54, 23),
            Unit.CORSAIR,
            1,
            0,
            0,
            iGameTurn,
            5,
            0,
            outerSeaSpawn,
            text("TXT_KEY_BARBARIAN_NAMES_BARBARY_PIRATES"),
        )
    if DateTurn.i1200AD <= iGameTurn < DateTurn.i1500AD:
        spawnPirate(
            Civ.BARBARIAN,
            (9, 15),
            (55, 33),
            Unit.COGGE,
            1,
            Unit.SWORDSMAN,
            2,
            iGameTurn,
            10,
            5,
            outerSeaSpawn,
        )
    elif iGameTurn >= DateTurn.i1500AD:
        spawnPirate(
            Civ.BARBARIAN,
            (9, 15),
            (55, 33),
            Unit.GALLEON,
            1,
            Unit.MUSKETMAN,
            2,
            iGameTurn,
            10,
            5,
            outerSeaSpawn,
        )

    # Germanic Barbarians throughout Western Europe (France, Germany)
    if iGameTurn < DateTurn.i600AD:
        spawnUnits(
            Civ.BARBARIAN,
            (43, 42),
            (50, 50),
            Unit.AXEMAN,
            1,
            iGameTurn,
            11,
            1,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES"),
        )
        if Civ.FRANCE == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (42, 40),
                (56, 48),
                Unit.AXEMAN,
                1,
                iGameTurn,
                9,
                3,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (45, 45),
                (60, 55),
                Unit.SPEARMAN,
                1,
                iGameTurn,
                18,
                7,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES"),
            )
    elif DateTurn.i600AD <= iGameTurn < DateTurn.i800AD:
        spawnUnits(
            Civ.BARBARIAN,
            (43, 42),
            (50, 50),
            Unit.AXEMAN,
            1,
            iGameTurn,
            9,
            2,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (42, 40),
            (56, 48),
            Unit.AXEMAN,
            1,
            iGameTurn,
            11,
            4,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES"),
        )
        if Civ.FRANCE == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (43, 42),
                (50, 50),
                Unit.AXEMAN,
                1,
                iGameTurn,
                9,
                3,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (45, 45),
                (60, 55),
                Unit.SPEARMAN,
                1 + iHandicap,
                iGameTurn,
                11,
                4,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (46, 48),
                (62, 55),
                Unit.AXEMAN,
                1 + iHandicap,
                iGameTurn,
                14,
                9,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES"),
            )

    # Longobards in Italy
    if DateTurn.i632AD <= iGameTurn <= DateTurn.i800AD:
        spawnUnits(
            Civ.BARBARIAN,
            (49, 33),
            (53, 36),
            Unit.AXEMAN,
            1 + iHandicap,
            iGameTurn,
            10,
            3,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_LONGOBARDS"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (49, 33),
            (53, 36),
            Unit.SPEARMAN,
            1,
            iGameTurn,
            12,
            0,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_LONGOBARDS"),
        )

    # Visigoths in Iberia
    if DateTurn.i712AD <= iGameTurn <= DateTurn.i892AD:
        spawnUnits(
            Civ.BARBARIAN,
            (22, 21),
            (26, 25),
            Unit.AXEMAN,
            1,
            iGameTurn,
            7,
            0,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_VISIGOTHS"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (23, 23),
            (27, 28),
            Unit.SPEARMAN,
            1,
            iGameTurn,
            7,
            3,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_VISIGOTHS"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (26, 27),
            (31, 32),
            Unit.MOUNTED_INFANTRY,
            1,
            iGameTurn,
            9,
            5,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_VISIGOTHS"),
        )
        if Civ.CORDOBA == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (24, 31),
                (27, 34),
                Unit.AXEMAN,
                1 + iHandicap,
                iGameTurn,
                7,
                0,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_VISIGOTHS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (27, 28),
                (31, 36),
                Unit.MOUNTED_INFANTRY,
                1,
                iGameTurn,
                6,
                3,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_VISIGOTHS"),
            )

    # Berbers in North Africa
    if DateTurn.i700AD <= iGameTurn < DateTurn.i1020AD:
        # Tunesia
        spawnUnits(
            Civ.BARBARIAN,
            (28, 10),
            (35, 14),
            Unit.HORSE_ARCHER,
            1 + iHandicap,
            iGameTurn,
            8,
            0,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_BERBERS"),
        )
        # Morocco
        if Civ.CORDOBA == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (21, 3),
                (27, 12),
                Unit.HORSE_ARCHER,
                1,
                iGameTurn,
                9,
                0,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_BERBERS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (22, 3),
                (27, 10),
                Unit.AXEMAN,
                1,
                iGameTurn,
                11,
                5,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_BERBERS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (23, 3),
                (27, 8),
                Unit.SPEARMAN,
                1,
                iGameTurn,
                7,
                3,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_BERBERS"),
            )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (22, 3),
                (27, 10),
                Unit.AXEMAN,
                1,
                iGameTurn,
                14,
                5,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_BERBERS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (23, 3),
                (27, 8),
                Unit.SPEARMAN,
                1,
                iGameTurn,
                8,
                3,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_BERBERS"),
            )

    # Avars in the Carpathian Basin
    if DateTurn.i632AD <= iGameTurn < DateTurn.i800AD:
        spawnUnits(
            Civ.BARBARIAN,
            (60, 30),
            (75, 40),
            Unit.HORSE_ARCHER,
            1,
            iGameTurn,
            5,
            0,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_AVARS"),
        )
        if Civ.BULGARIA == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (66, 26),
                (73, 29),
                Unit.HORSE_ARCHER,
                1 + iHandicap,
                iGameTurn,
                6,
                1,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_AVARS"),
            )

    # Early barbs for Byzantium:
    if iGameTurn < DateTurn.i640AD:
        # Pre-Bulgarian Slavs in the Balkans
        spawnUnits(
            Civ.BARBARIAN,
            (68, 18),
            (78, 28),
            Unit.AXEMAN,
            1,
            iGameTurn,
            8,
            0,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_SOUTHERN_SLAVS"),
        )
        if Civ.BYZANTIUM == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (64, 21),
                (75, 25),
                Unit.AXEMAN,
                1 + iHandicap,
                iGameTurn,
                11,
                3,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SOUTHERN_SLAVS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (68, 18),
                (78, 28),
                Unit.SPEARMAN,
                1,
                iGameTurn,
                8,
                0,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SOUTHERN_SLAVS"),
            )
        # Sassanids in Anatolia
        spawnUnits(
            Civ.BARBARIAN,
            (90, 15),
            (99, 28),
            Unit.LANCER,
            1,
            iGameTurn,
            6,
            2,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_SASSANIDS"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (94, 19),
            (98, 26),
            Unit.LANCER,
            1,
            iGameTurn,
            9,
            1,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_SASSANIDS"),
        )
        if Civ.BYZANTIUM == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (90, 15),
                (99, 28),
                Unit.LANCER,
                1,
                iGameTurn,
                6,
                2,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SASSANIDS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (94, 19),
                (98, 26),
                Unit.LANCER,
                1 + iHandicap,
                iGameTurn,
                9,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SASSANIDS"),
            )
    # Barbs in NW Greece
    if iGameTurn < DateTurn.i720AD:
        spawnUnits(
            Civ.BARBARIAN,
            (66, 21),
            (69, 28),
            Unit.AXEMAN,
            1,
            iGameTurn,
            9,
            3,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
        )
        if Civ.BYZANTIUM == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (66, 21),
                (69, 28),
                Unit.SPEARMAN,
                1 + iHandicap,
                iGameTurn,
                9,
                3,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
            )

    # Serbs in the Southern Balkans
    if DateTurn.i1025AD <= iGameTurn < DateTurn.i1282AD:
        if Civ.BYZANTIUM == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (67, 24),
                (73, 28),
                Unit.AXEMAN,
                1,
                iGameTurn,
                9,
                3,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SERBS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (67, 24),
                (73, 28),
                Unit.LANCER,
                1 + iHandicap,
                iGameTurn,
                11,
                7,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SERBS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (69, 25),
                (71, 29),
                Unit.SWORDSMAN,
                1,
                iGameTurn,
                7,
                4,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SERBS"),
            )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (67, 24),
                (73, 28),
                Unit.AXEMAN,
                1,
                iGameTurn,
                9,
                3,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SERBS"),
            )

    # Khazars
    if DateTurn.i660AD <= iGameTurn < DateTurn.i864AD:
        spawnUnits(
            Civ.BARBARIAN,
            (88, 31),
            (99, 40),
            Unit.AXEMAN,
            1,
            iGameTurn,
            8,
            0,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_KHAZARS"),
        )
    elif DateTurn.i864AD <= iGameTurn < DateTurn.i920AD:
        if Civ.KIEV == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (88, 31),
                (99, 40),
                Unit.AXEMAN,
                1,
                iGameTurn,
                7,
                2,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_KHAZARS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (88, 31),
                (99, 40),
                Unit.SPEARMAN,
                1,
                iGameTurn,
                5,
                2,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_KHAZARS"),
            )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (88, 31),
                (99, 40),
                Unit.AXEMAN,
                1,
                iGameTurn,
                11,
                2,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_KHAZARS"),
            )

    # Pechenegs
    if DateTurn.i920AD <= iGameTurn < DateTurn.i1040AD:
        # in the Rus
        spawnUnits(
            Civ.BARBARIAN,
            (89, 34),
            (97, 40),
            Unit.STEPPE_HORSE_ARCHER,
            1,
            iGameTurn,
            8,
            3,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_PECHENEGS"),
        )
        if Civ.KIEV == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (91, 35),
                (99, 44),
                Unit.STEPPE_HORSE_ARCHER,
                1 + iHandicap,
                iGameTurn,
                5,
                1,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_PECHENEGS"),
            )
        # in Hungary
        spawnUnits(
            Civ.BARBARIAN,
            (66, 35),
            (75, 42),
            Unit.STEPPE_HORSE_ARCHER,
            1,
            iGameTurn,
            9,
            1,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_PECHENEGS"),
        )
        if Civ.HUNGARY == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (66, 35),
                (75, 42),
                Unit.STEPPE_HORSE_ARCHER,
                1 + iHandicap,
                iGameTurn,
                9,
                1,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_PECHENEGS"),
            )
        # in Bulgaria
        elif Civ.BULGARIA == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (77, 31),
                (79, 33),
                Unit.STEPPE_HORSE_ARCHER,
                2 + iHandicap,
                iGameTurn,
                5,
                1,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_PECHENEGS"),
            )

    # Cumans and Kipchaks
    elif DateTurn.i1040AD <= iGameTurn < DateTurn.i1200AD:
        # in the Rus
        if Civ.KIEV == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (89, 34),
                (99, 40),
                Unit.STEPPE_HORSE_ARCHER,
                2,
                iGameTurn,
                7,
                5,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_CUMANS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (90, 33),
                (97, 44),
                Unit.STEPPE_HORSE_ARCHER,
                2 + iHandicap,
                iGameTurn,
                9,
                1,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_KIPCHAKS"),
            )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (89, 34),
                (99, 40),
                Unit.STEPPE_HORSE_ARCHER,
                1,
                iGameTurn,
                7,
                5,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_CUMANS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (90, 33),
                (97, 44),
                Unit.STEPPE_HORSE_ARCHER,
                1,
                iGameTurn,
                9,
                1,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_KIPCHAKS"),
            )
        # in Hungary
        spawnUnits(
            Civ.BARBARIAN,
            (64, 33),
            (77, 43),
            Unit.STEPPE_HORSE_ARCHER,
            1,
            iGameTurn,
            7,
            1,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_CUMANS"),
        )
        if Civ.HUNGARY == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (64, 33),
                (77, 43),
                Unit.STEPPE_HORSE_ARCHER,
                1,
                iGameTurn,
                7,
                1,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_CUMANS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (66, 35),
                (75, 42),
                Unit.STEPPE_HORSE_ARCHER,
                1,
                iGameTurn,
                9,
                4,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_KIPCHAKS"),
            )
        # in Bulgaria
        if Civ.BULGARIA == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (78, 32),
                (80, 34),
                Unit.STEPPE_HORSE_ARCHER,
                1,
                iGameTurn,
                7,
                3,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_CUMANS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (78, 32),
                (80, 34),
                Unit.STEPPE_HORSE_ARCHER,
                1,
                iGameTurn,
                7,
                3,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_KIPCHAKS"),
            )

    # Vikings on ships
    if Civ.NORWAY == iHuman:  # Humans can properly go viking without help
        pass
    elif DateTurn.i780AD <= iGameTurn < DateTurn.i1000AD:
        if Civ.FRANCE == iHuman:
            spawnVikings(
                Civ.BARBARIAN,
                (37, 48),
                (50, 54),
                Unit.VIKING_BERSERKER,
                2,
                iGameTurn,
                8,
                0,
                outerSeaSpawn,
                text("TXT_KEY_BARBARIAN_NAMES_VIKINGS"),
            )
        else:
            spawnVikings(
                Civ.BARBARIAN,
                (37, 48),
                (50, 54),
                Unit.VIKING_BERSERKER,
                1,
                iGameTurn,
                8,
                0,
                outerSeaSpawn,
                text("TXT_KEY_BARBARIAN_NAMES_VIKINGS"),
            )

    # Swedish Crusades
    elif DateTurn.i1150AD <= iGameTurn < DateTurn.i1210AD:
        spawnVikings(
            Civ.BARBARIAN,
            (71, 62),
            (76, 65),
            Unit.VIKING_BERSERKER,
            2,
            iGameTurn,
            6,
            1,
            outerSeaSpawn,
            text("TXT_KEY_BARBARIAN_NAMES_SWEDES"),
        )

    # Chudes in Finland and Estonia
    if DateTurn.i864AD <= iGameTurn < DateTurn.i1150AD:
        spawnUnits(
            Civ.BARBARIAN,
            (72, 67),
            (81, 72),
            Unit.AXEMAN,
            1,
            iGameTurn,
            7,
            0,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_CHUDES"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (74, 60),
            (76, 63),
            Unit.AXEMAN,
            1,
            iGameTurn,
            11,
            3,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_CHUDES"),
        )

    # Livonian Order as barbs in the area before the Prussian spawn, but only if Prussia is AI (no need for potentially gained extra units for the human player)
    # Also pre-Lithanian barbs for human Prussia a couple turns before the Lithuanian spawn
    if Civ.PRUSSIA == iHuman:
        if DateTurn.i1224AD <= iGameTurn < DateTurn.i1236AD:
            spawnUnits(
                Civ.BARBARIAN,
                (73, 56),
                (76, 61),
                Unit.AXEMAN,
                1,
                iGameTurn,
                2,
                1,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_BALTICS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (72, 54),
                (75, 59),
                Unit.AXEMAN,
                1,
                iGameTurn,
                2,
                1,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_BALTICS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (73, 56),
                (76, 61),
                Unit.HORSE_ARCHER,
                1 + iHandicap,
                iGameTurn,
                2,
                1,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_BALTICS"),
            )
    elif DateTurn.i1200AD <= iGameTurn < DateTurn.i1224AD:
        spawnUnits(
            Civ.BARBARIAN,
            (73, 57),
            (76, 61),
            Unit.TEUTONIC,
            1,
            iGameTurn,
            4,
            3,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_SWORD_BRETHEN"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (73, 57),
            (76, 61),
            Unit.SWORDSMAN,
            1,
            iGameTurn,
            4,
            1,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_SWORD_BRETHEN"),
        )

    # Couple melee barb units in Ireland:
    if DateTurn.i800AD <= iGameTurn < DateTurn.i900AD:
        spawnUnits(
            Civ.BARBARIAN,
            (28, 56),
            (33, 62),
            Unit.AXEMAN,
            1,
            iGameTurn,
            7,
            3,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_IRISH"),
        )

    # Anglo-Saxons before the Danish 1st UHV (Conquer England)
    elif DateTurn.i970AD <= iGameTurn < DateTurn.i1050AD:
        if Civ.DENMARK == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (36, 53),
                (41, 59),
                Unit.AXEMAN,
                1,
                iGameTurn,
                8,
                5,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_ANGLO_SAXONS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (33, 48),
                (38, 54),
                Unit.AXEMAN,
                1,
                iGameTurn,
                5,
                2,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_ANGLO_SAXONS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (33, 48),
                (38, 54),
                Unit.SWORDSMAN,
                1,
                iGameTurn,
                11,
                6,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_ANGLO_SAXONS"),
            )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (33, 48),
                (38, 54),
                Unit.AXEMAN,
                1,
                iGameTurn,
                5,
                2,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_ANGLO_SAXONS"),
            )

    # Scots to keep England busy, but only if Scotland is dead
    if not gc.getPlayer(Civ.SCOTLAND).isAlive():
        if DateTurn.i1060AD <= iGameTurn < DateTurn.i1320AD:
            if Civ.ENGLAND == iHuman:
                spawnUnits(
                    Civ.BARBARIAN,
                    (39, 62),
                    (44, 66),
                    Unit.HIGHLANDER,
                    2,
                    iGameTurn,
                    11,
                    0,
                    forcedInvasion,
                    UnitAITypes.UNITAI_ATTACK,
                    text("TXT_KEY_BARBARIAN_NAMES_SCOTS"),
                )
            else:
                spawnUnits(
                    Civ.BARBARIAN,
                    (39, 62),
                    (44, 66),
                    Unit.HIGHLANDER,
                    1,
                    iGameTurn,
                    11,
                    0,
                    forcedInvasion,
                    UnitAITypes.UNITAI_ATTACK,
                    text("TXT_KEY_BARBARIAN_NAMES_SCOTS"),
                )
        elif DateTurn.i1320AD <= iGameTurn < DateTurn.i1500AD:
            if Civ.ENGLAND == iHuman:
                spawnUnits(
                    Civ.BARBARIAN,
                    (39, 62),
                    (44, 66),
                    Unit.HIGHLANDER,
                    2,
                    iGameTurn,
                    9,
                    0,
                    forcedInvasion,
                    UnitAITypes.UNITAI_ATTACK,
                    text("TXT_KEY_BARBARIAN_NAMES_SCOTS"),
                )
                spawnUnits(
                    Civ.BARBARIAN,
                    (39, 64),
                    (44, 67),
                    Unit.HIGHLANDER,
                    2 + iHandicap,
                    iGameTurn,
                    17,
                    4,
                    forcedInvasion,
                    UnitAITypes.UNITAI_ATTACK,
                    text("TXT_KEY_BARBARIAN_NAMES_SCOTS"),
                )
            else:
                spawnUnits(
                    Civ.BARBARIAN,
                    (39, 64),
                    (44, 67),
                    Unit.HIGHLANDER,
                    2,
                    iGameTurn,
                    17,
                    4,
                    forcedInvasion,
                    UnitAITypes.UNITAI_ATTACK,
                    text("TXT_KEY_BARBARIAN_NAMES_SCOTS"),
                )

    # Welsh in Britain
    if DateTurn.i1060AD <= iGameTurn < DateTurn.i1160AD:
        if Civ.ENGLAND == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (37, 53),
                (39, 57),
                Unit.WELSH_LONGBOWMAN,
                1,
                iGameTurn,
                7,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_WELSH"),
            )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (37, 53),
                (39, 57),
                Unit.WELSH_LONGBOWMAN,
                1,
                iGameTurn,
                13,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_WELSH"),
            )
    elif DateTurn.i1160AD <= iGameTurn < DateTurn.i1452AD:
        if Civ.ENGLAND == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (37, 53),
                (39, 57),
                Unit.WELSH_LONGBOWMAN,
                2 + iHandicap,
                iGameTurn,
                12,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_WELSH"),
            )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (37, 53),
                (39, 57),
                Unit.WELSH_LONGBOWMAN,
                1,
                iGameTurn,
                9,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_WELSH"),
            )

    # Magyars (preceeding Hungary)
    if DateTurn.i840AD <= iGameTurn < DateTurn.i892AD:
        spawnUnits(
            Civ.BARBARIAN,
            (54, 38),
            (61, 45),
            Unit.HORSE_ARCHER,
            1,
            iGameTurn,
            4,
            1,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_MAGYARS"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (66, 26),
            (73, 29),
            Unit.HORSE_ARCHER,
            1,
            iGameTurn,
            4,
            2,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_MAGYARS"),
        )
        if Civ.BULGARIA == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (77, 31),
                (80, 34),
                Unit.HORSE_ARCHER,
                2 + iHandicap,
                iGameTurn,
                5,
                0,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_MAGYARS"),
            )
        elif Civ.GERMANY == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (54, 38),
                (61, 45),
                Unit.HORSE_ARCHER,
                2 + iHandicap,
                iGameTurn,
                5,
                3,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_MAGYARS"),
            )

    # Wends in NE Germany
    if DateTurn.i860AD <= iGameTurn < DateTurn.i1053AD:
        if Civ.GERMANY == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (55, 49),
                (60, 56),
                Unit.AXEMAN,
                1,
                iGameTurn,
                6,
                1,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_WENDS"),
            )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (55, 49),
                (60, 56),
                Unit.AXEMAN,
                1,
                iGameTurn,
                8,
                1,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_WENDS"),
            )

    # Great Slav Rising in 983AD
    if (DateTurn.i983AD - 1) <= iGameTurn < (DateTurn.i983AD + 1):
        if Civ.GERMANY == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (53, 48),
                (59, 55),
                Unit.AXEMAN,
                2,
                iGameTurn,
                2,
                0,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_WENDS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (53, 48),
                (59, 55),
                Unit.SPEARMAN,
                1,
                iGameTurn,
                2,
                0,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_WENDS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (53, 48),
                (59, 55),
                Unit.SWORDSMAN,
                1,
                iGameTurn,
                2,
                0,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_WENDS"),
            )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (53, 48),
                (59, 55),
                Unit.AXEMAN,
                1,
                iGameTurn,
                2,
                0,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_WENDS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (53, 48),
                (59, 55),
                Unit.SPEARMAN,
                1,
                iGameTurn,
                2,
                0,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_WENDS"),
            )

    # Barbs in the middle east
    if DateTurn.i700AD <= iGameTurn <= DateTurn.i1300AD:
        if not gc.getTeam(gc.getPlayer(Civ.ARABIA).getTeam()).isHasTech(Technology.FARRIERS):
            spawnUnits(
                Civ.BARBARIAN,
                (94, 0),
                (99, 3),
                Unit.HORSE_ARCHER,
                1,
                iGameTurn,
                11,
                3,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_BEDUINS"),
            )
            if gc.getPlayer(Civ.ARABIA).isHuman():
                spawnUnits(
                    Civ.BARBARIAN,
                    (94, 0),
                    (99, 3),
                    Unit.HORSE_ARCHER,
                    1 + iHandicap,
                    iGameTurn,
                    11,
                    3,
                    outerInvasion,
                    UnitAITypes.UNITAI_ATTACK,
                    text("TXT_KEY_BARBARIAN_NAMES_BEDUINS"),
                )
                spawnUnits(
                    Civ.BARBARIAN,
                    (92, 1),
                    (98, 4),
                    Unit.HORSE_ARCHER,
                    1,
                    iGameTurn,
                    8,
                    1,
                    forcedInvasion,
                    UnitAITypes.UNITAI_ATTACK,
                    text("TXT_KEY_BARBARIAN_NAMES_BEDUINS"),
                )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (94, 0),
                (99, 3),
                Unit.BEDOUIN,
                1,
                iGameTurn,
                10,
                2,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_BEDUINS"),
            )
            if gc.getPlayer(Civ.ARABIA).isHuman():
                spawnUnits(
                    Civ.BARBARIAN,
                    (94, 0),
                    (99, 3),
                    Unit.BEDOUIN,
                    1 + iHandicap,
                    iGameTurn,
                    10,
                    2,
                    outerInvasion,
                    UnitAITypes.UNITAI_ATTACK,
                    text("TXT_KEY_BARBARIAN_NAMES_BEDUINS"),
                )
                spawnUnits(
                    Civ.BARBARIAN,
                    (95, 1),
                    (98, 5),
                    Unit.BEDOUIN,
                    1,
                    iGameTurn,
                    7,
                    3,
                    forcedInvasion,
                    UnitAITypes.UNITAI_ATTACK,
                    text("TXT_KEY_BARBARIAN_NAMES_BEDUINS"),
                )

    # Banu Hilal and Bani Hassan, in Morocco and Tunesia
    if DateTurn.i1040AD <= iGameTurn < DateTurn.i1229AD:
        if Civ.MOROCCO == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (40, 10),
                (44, 14),
                Unit.BEDOUIN,
                2 + iHandicap,
                iGameTurn,
                11,
                2,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_BANU_HILAL"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (44, 1),
                (50, 8),
                Unit.TOUAREG,
                2 + iHandicap,
                iGameTurn,
                8,
                5,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_BANU_HILAL"),
            )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (40, 10),
                (44, 14),
                Unit.BEDOUIN,
                1,
                iGameTurn,
                11,
                2,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_BANU_HILAL"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (44, 1),
                (50, 8),
                Unit.TOUAREG,
                1,
                iGameTurn,
                8,
                5,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_BANU_HILAL"),
            )
    if DateTurn.i1640AD <= iGameTurn < DateTurn.i1680AD:
        spawnUnits(
            Civ.BARBARIAN,
            (18, 1),
            (22, 3),
            Unit.BEDOUIN,
            5 + iHandicap * 2,
            iGameTurn,
            3,
            1,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_BANI_HASSAN"),
        )

    # Pre Mongols to keep Kiev busy
    if DateTurn.i900AD <= iGameTurn < DateTurn.i1020AD:
        spawnUnits(
            Civ.BARBARIAN,
            (93, 35),
            (99, 44),
            Unit.HORSE_ARCHER,
            1,
            iGameTurn,
            13,
            1,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
        )
    elif DateTurn.i1020AD <= iGameTurn < DateTurn.i1236AD:
        spawnUnits(
            Civ.BARBARIAN,
            (93, 35),
            (99, 44),
            Unit.HORSE_ARCHER,
            1,
            iGameTurn,
            9,
            5,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
        )
        if Civ.KIEV == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (94, 32),
                (97, 39),
                Unit.HORSE_ARCHER,
                2 + iHandicap,
                iGameTurn,
                10,
                1,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
            )

    # Barbs in Anatolia pre Seljuks (but after Sassanids)
    if DateTurn.i700AD <= iGameTurn < DateTurn.i1050AD:
        spawnUnits(
            Civ.BARBARIAN,
            (97, 20),
            (99, 26),
            Unit.HORSE_ARCHER,
            1,
            iGameTurn,
            10,
            1,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
        )
        spawnUnits(
            Civ.BARBARIAN,
            (95, 20),
            (99, 24),
            Unit.AXEMAN,
            1,
            iGameTurn,
            14,
            2,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
        )
        spawnUnits(
            Civ.BARBARIAN,
            (95, 22),
            (97, 26),
            Unit.SPEARMAN,
            1,
            iGameTurn,
            16,
            6,
            outerInvasion,
            UnitAITypes.UNITAI_ATTACK,
        )
        if Civ.BYZANTIUM == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (97, 20),
                (99, 26),
                Unit.HORSE_ARCHER,
                1 + iHandicap,
                iGameTurn,
                10,
                1,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
            )
            spawnUnits(
                Civ.BARBARIAN,
                (95, 20),
                (99, 24),
                Unit.AXEMAN,
                1,
                iGameTurn,
                14,
                2,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
            )
            spawnUnits(
                Civ.BARBARIAN,
                (95, 20),
                (99, 24),
                Unit.HORSE_ARCHER,
                1 + iHandicap,
                iGameTurn,
                14,
                2,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
            )
            spawnUnits(
                Civ.BARBARIAN,
                (95, 22),
                (97, 26),
                Unit.SPEARMAN,
                1,
                iGameTurn,
                16,
                6,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
            )
            spawnUnits(
                Civ.BARBARIAN,
                (95, 22),
                (97, 26),
                Unit.HORSE_ARCHER,
                1 + iHandicap,
                iGameTurn,
                16,
                6,
                outerInvasion,
                UnitAITypes.UNITAI_ATTACK,
            )

    # Seljuks
    if DateTurn.i1064AD <= iGameTurn < DateTurn.i1094AD:
        spawnUnits(
            Civ.BARBARIAN,
            (90, 21),
            (99, 28),
            Unit.SELJUK_LANCER,
            3,
            iGameTurn,
            3,
            0,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (90, 21),
            (99, 28),
            Unit.TURCOMAN_HORSE_ARCHER,
            1,
            iGameTurn,
            3,
            0,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (90, 21),
            (99, 28),
            Unit.SELJUK_CROSSBOW,
            1,
            iGameTurn,
            3,
            0,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (90, 21),
            (99, 28),
            Unit.SELJUK_SWORDSMAN,
            1,
            iGameTurn,
            3,
            0,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (92, 20),
            (99, 25),
            Unit.SELJUK_LANCER,
            3,
            iGameTurn,
            3,
            1,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (92, 20),
            (99, 25),
            Unit.TURCOMAN_HORSE_ARCHER,
            1,
            iGameTurn,
            3,
            1,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (92, 20),
            (99, 25),
            Unit.SELJUK_GUISARME,
            1,
            iGameTurn,
            3,
            1,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (92, 20),
            (99, 25),
            Unit.SELJUK_FOOTMAN,
            1,
            iGameTurn,
            3,
            1,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (95, 8),
            (99, 12),
            Unit.SELJUK_LANCER,
            2,
            iGameTurn,
            4,
            1,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (95, 8),
            (99, 12),
            Unit.SELJUK_CROSSBOW,
            1,
            iGameTurn,
            4,
            1,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
        )
        if Civ.BYZANTIUM == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (90, 21),
                (99, 28),
                Unit.SELJUK_LANCER,
                1,
                iGameTurn,
                3,
                0,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (90, 21),
                (99, 28),
                Unit.TURCOMAN_HORSE_ARCHER,
                1,
                iGameTurn,
                3,
                0,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (90, 21),
                (99, 28),
                Unit.SELJUK_CROSSBOW,
                1 + iHandicap,
                iGameTurn,
                3,
                0,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (90, 21),
                (99, 28),
                Unit.SELJUK_GUISARME,
                1,
                iGameTurn,
                3,
                0,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (90, 21),
                (99, 28),
                Unit.SELJUK_FOOTMAN,
                1 + iHandicap,
                iGameTurn,
                3,
                0,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (92, 20),
                (99, 25),
                Unit.SELJUK_LANCER,
                1,
                iGameTurn,
                3,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (92, 20),
                (99, 25),
                Unit.TURCOMAN_HORSE_ARCHER,
                1,
                iGameTurn,
                3,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (92, 20),
                (99, 25),
                Unit.SELJUK_GUISARME,
                1 + iHandicap,
                iGameTurn,
                3,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (92, 20),
                (99, 25),
                Unit.SELJUK_CROSSBOW,
                1,
                iGameTurn,
                3,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (92, 20),
                (99, 25),
                Unit.SELJUK_SWORDSMAN,
                1 + iHandicap,
                iGameTurn,
                3,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
            )
        elif Civ.ARABIA == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (95, 8),
                (99, 12),
                Unit.SELJUK_LANCER,
                1 + iHandicap,
                iGameTurn,
                4,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (95, 8),
                (99, 12),
                Unit.TURCOMAN_HORSE_ARCHER,
                1,
                iGameTurn,
                4,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (95, 8),
                (99, 12),
                Unit.SELJUK_GUISARME,
                1,
                iGameTurn,
                4,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_SELJUKS"),
            )

    # Danishmends
    if DateTurn.i1077AD <= iGameTurn < DateTurn.i1147AD:
        if Civ.BYZANTIUM == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (93, 20),
                (99, 22),
                Unit.TURCOMAN_HORSE_ARCHER,
                3 + iHandicap,
                iGameTurn,
                5,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_DANISHMENDS"),
            )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (93, 20),
                (99, 22),
                Unit.TURCOMAN_HORSE_ARCHER,
                2,
                iGameTurn,
                5,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_DANISHMENDS"),
            )

    # Mongols
    if DateTurn.i1236AD <= iGameTurn < DateTurn.i1288AD:
        # Kiev
        if Civ.KIEV == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (93, 32),
                (99, 42),
                Unit.MONGOL_KESHIK,
                5 + iHandicap,
                iGameTurn,
                4,
                0,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_MONGOLS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (94, 34),
                (99, 45),
                Unit.MONGOL_KESHIK,
                4 + iHandicap,
                iGameTurn,
                3,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_MONGOLS"),
            )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (93, 32),
                (99, 42),
                Unit.MONGOL_KESHIK,
                3,
                iGameTurn,
                4,
                0,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_MONGOLS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (94, 34),
                (99, 45),
                Unit.MONGOL_KESHIK,
                2,
                iGameTurn,
                3,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_MONGOLS"),
            )
        # Hungary
        if Civ.HUNGARY == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (71, 38),
                (75, 40),
                Unit.MONGOL_KESHIK,
                4 + iHandicap,
                iGameTurn,
                4,
                2,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_MONGOLS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (74, 35),
                (77, 37),
                Unit.MONGOL_KESHIK,
                2,
                iGameTurn,
                4,
                2,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_MONGOLS"),
            )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (71, 38),
                (75, 40),
                Unit.MONGOL_KESHIK,
                2,
                iGameTurn,
                4,
                2,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_MONGOLS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (74, 35),
                (77, 37),
                Unit.MONGOL_KESHIK,
                1,
                iGameTurn,
                4,
                2,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_MONGOLS"),
            )
        # Poland
        if Civ.POLAND == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (73, 43),
                (78, 47),
                Unit.MONGOL_KESHIK,
                5 + iHandicap,
                iGameTurn,
                4,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_MONGOLS"),
            )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (73, 43),
                (78, 47),
                Unit.MONGOL_KESHIK,
                2,
                iGameTurn,
                4,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_MONGOLS"),
            )
        # Bulgaria
        if Civ.BULGARIA == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (79, 32),
                (82, 35),
                Unit.MONGOL_KESHIK,
                3 + iHandicap,
                iGameTurn,
                4,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_MONGOLS"),
            )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (79, 32),
                (82, 35),
                Unit.MONGOL_KESHIK,
                2,
                iGameTurn,
                4,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_MONGOLS"),
            )
        # Moscow area
        spawnUnits(
            Civ.BARBARIAN,
            (89, 46),
            (95, 54),
            Unit.MONGOL_KESHIK,
            1,
            iGameTurn,
            4,
            0,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_MONGOLS"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (91, 48),
            (97, 53),
            Unit.MONGOL_KESHIK,
            2,
            iGameTurn,
            6,
            1,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_MONGOLS"),
        )
        # Middle East
        spawnUnits(
            Civ.BARBARIAN,
            (94, 20),
            (99, 26),
            Unit.MONGOL_KESHIK,
            2,
            iGameTurn,
            3,
            2,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_MONGOLS"),
        )
        spawnUnits(
            Civ.BARBARIAN,
            (92, 21),
            (97, 25),
            Unit.MONGOL_KESHIK,
            2,
            iGameTurn,
            6,
            1,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_MONGOLS"),
        )

    # Timurids, Tamerlane's conquests (aka Mongols, the return!)
    if (
        DateTurn.i1380AD <= iGameTurn <= DateTurn.i1431AD
    ):  # Timur started his first western campaigns in 1380AD
        # Eastern Europe
        spawnUnits(
            Civ.BARBARIAN,
            (85, 47),
            (99, 57),
            Unit.MONGOL_KESHIK,
            2,
            iGameTurn,
            7,
            0,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_TIMURIDS"),
        )
        # Anatolia
        if Civ.OTTOMAN == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (87, 17),
                (96, 24),
                Unit.MONGOL_KESHIK,
                4 + iHandicap,
                iGameTurn,
                4,
                0,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_TIMURIDS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (94, 18),
                (99, 26),
                Unit.MONGOL_KESHIK,
                6 + iHandicap,
                iGameTurn,
                5,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_TIMURIDS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (89, 17),
                (97, 22),
                Unit.MONGOL_KESHIK,
                3 + iHandicap,
                iGameTurn,
                4,
                2,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_TIMURIDS"),
            )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (87, 17),
                (96, 24),
                Unit.MONGOL_KESHIK,
                2,
                iGameTurn,
                4,
                0,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_TIMURIDS"),
            )
            spawnUnits(
                Civ.BARBARIAN,
                (94, 18),
                (99, 26),
                Unit.MONGOL_KESHIK,
                3,
                iGameTurn,
                5,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_TIMURIDS"),
            )
        # Arabia
        if Civ.ARABIA == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (96, 9),
                (99, 15),
                Unit.MONGOL_KESHIK,
                5 + iHandicap,
                iGameTurn,
                4,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_TIMURIDS"),
            )
        else:
            spawnUnits(
                Civ.BARBARIAN,
                (96, 9),
                (99, 15),
                Unit.MONGOL_KESHIK,
                2,
                iGameTurn,
                4,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_TIMURIDS"),
            )

    # Nogais
    if DateTurn.i1500AD <= iGameTurn <= DateTurn.i1600AD:
        spawnUnits(
            Civ.BARBARIAN,
            (93, 38),
            (99, 54),
            Unit.HORSE_ARCHER,
            3,
            iGameTurn,
            7,
            1,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_NOGAIS"),
        )
        if Civ.MOSCOW == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (93, 38),
                (99, 54),
                Unit.HORSE_ARCHER,
                2 + iHandicap,
                iGameTurn,
                7,
                1,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_NOGAIS"),
            )

    # Kalmyks
    elif DateTurn.i1600AD <= iGameTurn <= DateTurn.i1715AD:
        spawnUnits(
            Civ.BARBARIAN,
            (93, 38),
            (99, 54),
            Unit.MONGOL_KESHIK,
            3,
            iGameTurn,
            7,
            0,
            forcedInvasion,
            UnitAITypes.UNITAI_ATTACK,
            text("TXT_KEY_BARBARIAN_NAMES_KALMYKS"),
        )
        if Civ.MOSCOW == iHuman:
            spawnUnits(
                Civ.BARBARIAN,
                (93, 38),
                (99, 54),
                Unit.MONGOL_KESHIK,
                3 + iHandicap,
                iGameTurn,
                7,
                0,
                forcedInvasion,
                UnitAITypes.UNITAI_ATTACK,
                text("TXT_KEY_BARBARIAN_NAMES_KALMYKS"),
            )

    # Independent/barb city spawns and minor nations:
    doIndependentCities(iGameTurn)

    if iGameTurn == 1:
        setupMinorNation()
    doMinorNations(iGameTurn)


def doIndependentCities(iGameTurn):
    if iGameTurn in dIndependentCities.keys():
        for tCity in dIndependentCities[iGameTurn]:
            lVariations, iCiv, iPop, iUnit, iNumUnits, iReligion, iWorkers = tCity
            iChosenCity = -1
            iRand = percentage()
            for iCity in range(len(lVariations)):
                if iRand < lVariations[iCity][2]:
                    iChosenCity = iCity
                    break
                iRand -= lVariations[iCity][2]
            if iChosenCity == -1:
                continue
            tCoords, sName, iPos = lVariations[iChosenCity]
            foundCity(iCiv, tCoords, sName, iPop, iUnit, iNumUnits, iReligion, iWorkers)


def foundCity(iCiv, tCoords, name, iPopulation, iUnitType, iNumUnits, iReligion, iWorkers):
    if checkRegion(tCoords):
        gc.getPlayer(iCiv).found(tCoords[0], tCoords[1])
        city = gc.getMap().plot(tCoords[0], tCoords[1]).getPlotCity()
        city.setName(name, False)
        if iPopulation != 1:
            city.setPopulation(iPopulation)
        if iNumUnits > 0:
            make_units(iCiv, iUnitType, tCoords, iNumUnits)
        if iReligion > -1:
            city.setHasReligion(iReligion, True, True, False)
        if iWorkers > 0:
            make_units(iCiv, Unit.WORKER, tCoords, iWorkers)


def checkRegion(tCoords):
    cityPlot = gc.getMap().plot(tCoords[0], tCoords[1])

    # checks if the plot already belongs to someone
    if cityPlot.isOwned():
        if cityPlot.getOwner() != Civ.BARBARIAN:
            return False

    # checks the surroundings for cities
    if plots.surrounding(tCoords).cities().entities():
        return False
    return True


def spawnUnits(
    iCiv,
    tTopLeft,
    tBottomRight,
    iUnitType,
    iNumUnits,
    iTurn,
    iPeriod,
    iRest,
    function,
    unit_ai,
    unit_name=None,
):
    if (iTurn % iPeriod) == iRest:
        plotList = squareSearch(tTopLeft, tBottomRight, function, [])
        if plotList:
            tPlot = random_entry(plotList)
            if tPlot is not None:
                make_units(iCiv, iUnitType, tPlot, iNumUnits, unit_ai, unit_name)


def spawnVikings(
    iCiv,
    tTopLeft,
    tBottomRight,
    iUnitType,
    iNumUnits,
    iTurn,
    iPeriod,
    iRest,
    function,
    unit_name=None,
):
    if (iTurn % iPeriod) == iRest:
        plotList = squareSearch(tTopLeft, tBottomRight, function, [])
        if plotList:
            tPlot = random_entry(plotList)
            if tPlot is not None:
                make_unit(iCiv, Unit.GALLEY, tPlot, UnitAITypes.UNITAI_ASSAULT_SEA, unit_name)
                make_units(iCiv, iUnitType, tPlot, iNumUnits, UnitAITypes.UNITAI_ATTACK, unit_name)


def spawnPirate(
    iCiv,
    tTopLeft,
    tBottomRight,
    iShipType,
    iNumShips,
    iFighterType,
    iNumFighters,
    iTurn,
    iPeriod,
    iRest,
    function,
    unit_name=None,
):
    if (iTurn % iPeriod) == iRest:
        plotList = squareSearch(tTopLeft, tBottomRight, function, [])
        if plotList:
            tPlot = random_entry(plotList)
            if tPlot is not None:
                make_units(
                    iCiv, iShipType, tPlot, iNumShips, UnitAITypes.UNITAI_ATTACK_SEA, unit_name
                )
                make_units(
                    iCiv,
                    iFighterType,
                    tPlot,
                    iNumFighters,
                    UnitAITypes.UNITAI_ATTACK,
                    unit_name,
                )


def killNeighbours(tCoords):
    "Kills all units in the neigbbouring tiles of plot (as well as plot it) so late starters have some space."
    for unit in plots.surrounding(tCoords).units().entities():
        unit.kill(False, Civ.BARBARIAN)


def onImprovementDestroyed(iX, iY):
    # getHandicapType: Viceroy=0, Monarch=1, Emperor=2)
    iHandicap = gc.getGame().getHandicapType()
    iTurn = turn()
    if iTurn > DateTurn.i1500AD:
        iBarbUnit = Unit.MUSKETMAN
    elif iTurn > DateTurn.i1284AD:
        iBarbUnit = Unit.ARQUEBUSIER
    elif iTurn > DateTurn.i840AD:
        iBarbUnit = Unit.HORSE_ARCHER
    else:
        iBarbUnit = Unit.SPEARMAN
    spawnUnits(
        Civ.BARBARIAN,
        (iX - 1, iY - 1),
        (iX + 1, iY + 1),
        iBarbUnit,
        1 + iHandicap,
        1,
        1,
        0,
        outerInvasion,
        UnitAITypes.UNITAI_ATTACK,
    )


def setupMinorNation():
    for lNation in lMinorNations:
        iNextRevolt = lNation[3][0]
        while iNextRevolt in data.minor_revolt_dates:
            iNextRevolt = lNation[3][0] - 3 + rand(6)
        iNationIndex = lMinorNations.index(lNation)
        data.minor_revolt_dates[iNationIndex] = iNextRevolt


def doMinorNations(iGameTurn):
    if iGameTurn in data.minor_revolt_dates:
        lNation = lMinorNations[data.minor_revolt_dates.index(iGameTurn)]
        lRevolts = lNation[3]
        for iRevoltDate in lRevolts:
            if (iRevoltDate - 3 <= iGameTurn) and (iRevoltDate + 3 >= iGameTurn):
                iRevoltIndex = lRevolts.index(iRevoltDate)
                break
        # loop over all the province tiles to find the cities revolting
        lPlayersOwning = [0] * civilizations().main().len()
        iProvince = lNation[0]
        for iI in range(gc.getNumProvinceTiles(iProvince)):
            iX = gc.getProvinceX(iProvince, iI)
            iY = gc.getProvinceY(iProvince, iI)
            if gc.getMap().plot(iX, iY).isCity():
                iOwner = gc.getMap().plot(iX, iY).getPlotCity().getOwner()
                if -1 < iOwner < Civ.POPE:  # pope doesn't count here
                    if (
                        iOwner not in lNation[1]
                        and gc.getPlayer(iOwner).getStateReligion() not in lNation[2]
                    ):
                        lPlayersOwning[iOwner] += 1

        for iPlayer in civilizations().main().ids():
            if lPlayersOwning[iPlayer] > 0:
                if human() == iPlayer:
                    doRevoltHuman(iPlayer, iGameTurn, lNation, iRevoltIndex)
                else:
                    doRevoltAI(iPlayer, iGameTurn, lNation, iRevoltIndex)
        # setup next revolt
        iRevoltIndex += 1
        if iRevoltIndex < len(lNation[3]):
            iNextRevolt = lNation[3][iRevoltIndex] - 3 + rand(6)
            while iNextRevolt in data.minor_revolt_dates:
                iNextRevolt = lNation[3][iRevoltIndex] - 3 + rand(6)
            data.minor_revolt_dates[data.minor_revolt_dates.index(iGameTurn)] = iNextRevolt


def doRevoltAI(iPlayer, iGameTurn, lNation, iRevoltIndex):
    cityList = cities.owner(iPlayer).province(lNation[0]).entities()

    iNumGarrison = 0
    for iI in range(len(cityList)):
        iNumGarrison += getGarrasonSize(cityList[iI])

    # base rebellion odds: maximum 45%
    # odds considering minor nation strength - between 10 and 40
    iSuppressOdds = -lNation[4][iRevoltIndex]
    # stability odds: maximum 20 + lNation[4][iRevoltIndex]
    pPlayer = gc.getPlayer(iPlayer)
    iSuppressOdds += 20 + max(-10, min(pPlayer.getStability() * 2, lNation[4][iRevoltIndex]))
    # passive bonus from city garrison: maximum 15
    iSuppressOdds += min((3 * iNumGarrison) / len(cityList), 15)
    # AI bonus
    iSuppressOdds += 10

    # AI always cracks revolt: maximum 35%
    # with a crackdown you will get a turn of unrest and some unhappiness even if it succeeds.
    iSuppressOdds = 10
    iSuppressOdds += min((5 * iNumGarrison) / len(cityList), 25)

    # time to roll the dice
    if percentage_chance(iSuppressOdds, strict=True, reverse=True):
        # revolt suppressed
        for iI in range(len(cityList)):
            pCity = cityList[iI]
            pCity.changeHurryAngerTimer(10)
            pCity.changeOccupationTimer(1)
            makeRebels(pCity, lNation[5][iRevoltIndex], lNation[6][iRevoltIndex], lNation[7][1])
    else:
        # revolt succeeded
        iNewCiv = choice(INDEPENDENT_CIVS)
        for iI in range(len(cityList)):
            pCity = cityList[iI]
            tCity = (pCity.getX(), pCity.getY())
            cultureManager(tCity, 50, iNewCiv, iPlayer, False, True, True)
            flipUnitsInCitySecession(tCity, iNewCiv, iPlayer)
            setTempFlippingCity(tCity)
            flipCity(
                tCity, 0, 0, iNewCiv, [iPlayer]
            )  # by trade because by conquest may raze the city
            flipUnitsInCityAfter(getTempFlippingCity(), iNewCiv)


@popup_handler(7627)
def CounterReformationEvent(playerID, netUserData, popupReturn):
    iDecision = popupReturn.getButtonClicked()
    iNationIndex, iRevoltIndex = data.revolut_nation_index
    lNation = lMinorNations[iNationIndex]
    iPlayer = human()

    cityList = cities.owner(iPlayer).province(lNation[0]).entities()

    iNumGarrison = 0
    iBribeGold = 0
    for iI in range(len(cityList)):
        iNumGarrison += getGarrasonSize(cityList[iI])
        iBribeGold += 10 * cityList[iI].getPopulation()

    # raw suppress score
    iSuppressOdds = -lNation[4][iRevoltIndex]
    pPlayer = gc.getPlayer(iPlayer)
    iSuppressOdds += 20 + max(-10, min(pPlayer.getStability() * 2, lNation[4][iRevoltIndex]))
    iSuppressOdds += min((3 * iNumGarrison) / len(cityList), 15)

    # 2nd or 4th choice
    if iDecision in [1, 3]:
        iSuppressOdds += 10 + min((5 * iNumGarrison) / len(cityList), 25)

    # 3rd or 4th choice
    if iDecision in [2, 3]:
        iGovernment = pPlayer.getCivics(0)
        if iGovernment == Civic.DESPOTISM:
            iBribeOdds = 15
        elif iGovernment == Civic.FEUDAL_MONARCHY:
            iBribeOdds = 25
        elif iGovernment == Civic.DIVINE_MONARCHY:
            iBribeOdds = 30
        elif iGovernment == Civic.LIMITE_DMONARCHY:
            iBribeOdds = 25
        elif iGovernment == Civic.MERCHANT_REPUBLIC:
            iBribeOdds = 20
        iGold = pPlayer.getGold()
        if iGold < iBribeGold:
            iBribeOdds = (iBribeOdds * iGold) / (iBribeGold)
        pPlayer.setGold(iGold - min(iGold, iBribeGold))
        iSuppressOdds += iBribeOdds

    if percentage_chance(iSuppressOdds, strict=True, reverse=True):
        # revolt suppressed
        for iI in range(len(cityList)):
            pCity = cityList[iI]
            message(
                iPlayer,
                text("TXT_KEY_MINOR_NATION_REVOLT_SUPRESSED", pCity.getName()),
                color=MessageData.BLUE,
            )
            # cracking the rebels results in unhappiness in the general population:
            if iDecision in [1, 3]:
                pCity.changeHurryAngerTimer(10)
                pCity.changeOccupationTimer(1)
            # bribing their lords away from their cause angers the rebel militia further:
            if iDecision in [2, 3]:
                makeRebels(
                    pCity,
                    lNation[5][iRevoltIndex],
                    1 + lNation[6][iRevoltIndex],
                    lNation[7][1],
                )
            else:
                makeRebels(
                    pCity, lNation[5][iRevoltIndex], lNation[6][iRevoltIndex], lNation[7][1]
                )
    else:
        # revolt succeeded
        iNewCiv = choice(INDEPENDENT_CIVS)
        for iI in range(len(cityList)):
            pCity = cityList[iI]
            tCity = (pCity.getX(), pCity.getY())
            sNationName = text(lNation[7][1])
            message(
                iPlayer,
                text("TXT_KEY_MINOR_NATION_REVOLT_SUCCEEDED", sNationName, pCity.getName()),
                color=MessageData.ORANGE,
            )
            cultureManager(tCity, 50, iNewCiv, iPlayer, False, True, True)
            flipUnitsInCitySecession(tCity, iNewCiv, iPlayer)
            setTempFlippingCity(tCity)
            flipCity(
                tCity, 0, 0, iNewCiv, [iPlayer]
            )  # by trade because by conquest may raze the city
            flipUnitsInCityAfter(getTempFlippingCity(), iNewCiv)


# Absinthe: revolution choice effects:
# base chance: stability bonus adjusted with the revolt strength + base chance + passive military presence - revolt strength
# suppress with force: + base chance + military strength in the city. revolt +1 turn, unhappy +1 for 10 turns
# bribe the lords: + financial chance: costs 10 gold per population, suppression depends on the government Divine Monarchy (30%), Feudal or Limited (25%), Merchant (20%), Decentral (15%)
def doRevoltHuman(iPlayer, iGameTurn, lNation, iRevoltIndex):
    data.revolut_nation_index = [lMinorNations.index(lNation), iRevoltIndex]

    cityList = cities.owner(iPlayer).province(lNation[0]).entities()

    iNumGarrison = 0
    iBribeGold = 0
    for iI in range(len(cityList)):
        iNumGarrison += getGarrasonSize(cityList[iI])
        iBribeGold += 10 * cityList[iI].getPopulation()

    # base rebellion odds: maximum 35%
    # odds considering minor nation strength - usually 10, 20, 30, or 40
    iRawOdds = -lNation[4][iRevoltIndex]
    # stability odds: maximum 20 + lNation[4][iRevoltIndex]
    pPlayer = gc.getPlayer(iPlayer)
    iRawOdds += 20 + max(-10, min(pPlayer.getStability() * 2, lNation[4][iRevoltIndex]))
    # passive bonus from city garrison: maximum 15
    iRawOdds += min((3 * iNumGarrison) / len(cityList), 15)

    # odds adjusted by a crackdown: maximum 35%
    # with a crackdown you will get a turn of unrest and some unhappiness even if it succeeds.
    iCrackOdds = 10
    iCrackOdds += min((5 * iNumGarrison) / len(cityList), 25)

    # odds adjusted by bribery: maximum 30%
    # bribe the lords, cost 10 gold per population
    # suppression depends on the government Divine Monarchy (30%), Feudal or Limited (25%), Merchant (20%), Decentral (15%)
    iGovernment = pPlayer.getCivics(0)
    if iGovernment == Civic.DESPOTISM:
        iBribeOdds = 15
    elif iGovernment == Civic.FEUDAL_MONARCHY:
        iBribeOdds = 25
    elif iGovernment == Civic.DIVINE_MONARCHY:
        iBribeOdds = 30
    elif iGovernment == Civic.LIMITE_DMONARCHY:
        iBribeOdds = 25
    elif iGovernment == Civic.MERCHANT_REPUBLIC:
        iBribeOdds = 20
    iGold = pPlayer.getGold()
    if iGold < iBribeGold:
        iBribeOdds = (iBribeOdds * iGold) / (iBribeGold)
    iGold = min(iGold, iBribeGold)

    # values should be between 0 and 100
    iAllOdds = max(0, iRawOdds + iBribeOdds + iCrackOdds)
    iBribeOdds = max(0, iRawOdds + iBribeOdds)
    iCrackOdds = max(0, iRawOdds + iCrackOdds)
    iRawOdds = max(0, iRawOdds)

    rebel_name = text(lNation[7][0])
    event_popup(
        7627,
        text("TXT_KEY_MINOR_REBELLION_TITLE", rebel_name),
        text("TXT_KEY_MINOR_REBELLION_DESC", rebel_name),
        [
            text("TXT_KEY_MINOR_REBELLION_DO_NOTHING", iRawOdds),
            text("TXT_KEY_MINOR_REBELLION_CRACK", iCrackOdds),
            text("TXT_KEY_MINOR_REBELLION_BRIBE", iGold, iBribeGold, iBribeOdds),
            text("TXT_KEY_MINOR_REBELLION_ALL", iAllOdds),
        ],
    )


def getGarrasonSize(pCity):
    pPlot = gc.getMap().plot(pCity.getX(), pCity.getY())
    iOwner = pPlot.getOwner()
    if iOwner < 0:
        return 0
    iNumUnits = pPlot.getNumUnits()
    iDefenders = 0
    for i in range(iNumUnits):
        if pPlot.getUnit(i).getOwner() == iOwner:
            iDefenders += 1
    return iDefenders


def makeRebels(pCity, iUnit, iCount, szName):
    lAvailableFreeTiles = []
    lAvailableTiles = []
    for plot in (
        plots.surrounding(pCity)
        .filter(lambda p: p.isHills() or p.isFlatlands())
        .filter(lambda p: not p.isCity())
        .entities()
    ):
        if plot.getNumUnits() == 0:
            lAvailableFreeTiles.append(location(plot))
        else:
            lAvailableTiles.append(location(plot))

    if lAvailableFreeTiles:
        tPlot = choice(lAvailableFreeTiles)
    elif lAvailableTiles:
        # if all tiles are taken, select one tile at random and kill all units there
        tPlot = choice(lAvailableTiles)
        pPlot = gc.getMap().plot(tPlot[0], tPlot[1])
        iN = pPlot.getNumUnits()
        for i in range(iN):
            pPlot.getUnit(0).kill(False, Civ.BARBARIAN)
    else:
        return

    unit_name = text(szName)
    make_units(Civ.BARBARIAN, iUnit, tPlot, iCount, UnitAITypes.UNITAI_ATTACK, unit_name)
