# Rhye's and Fall of Civilization: Europe - Barbarian units and cities

from random import choice
from CvPythonExtensions import *
from CoreStructures import human
from CoreTypes import Civ, Civic, Religion, Technology, Unit, Province
import Popup
from PyUtils import percentage, percentage_chance, rand
import RFCUtils
from TimelineData import DateTurn
from StoredData import sd

from CoreData import civilizations
from MiscData import MessageData

gc = CyGlobalContext()
utils = RFCUtils.RFCUtils()
localText = CyTranslator()


# Independent and barbarians city spawns
# Key: tCity = variations (coordinates, actual city name, chance), owner, population size, defender type, number of defenders, religion, workers
# Notes: Indy cities start with zero-sized culture, barbs with normal culture
# 		Added some initial food reserves on founding cities, so even independents won't shrink on their first turn anymore
# 		Barbarian cities start with 2 additional defender units
# 		Walls (and other buildings) can be added with the onCityBuilt function, in RiseAndFall.py
# 500 AD
tTangier = (
    [((27, 16), "Tangier", 100)],
    Civ.INDEPENDENT_2.value,
    1,
    Unit.CORDOBAN_BERBER.value,
    2,
    -1,
    0,
)
tBordeaux = ([((37, 38), "Burdigala", 100)], Civ.BARBARIAN.value, 2, Unit.ARCHER.value, 0, -1, 0)
tAlger = (
    [((40, 16), "Alger", 60), ((34, 13), "Tlemcen", 40)],
    Civ.INDEPENDENT_3.value,
    1,
    Unit.ARCHER.value,
    1,
    Religion.CATHOLICISM.value,
    0,
)
tBarcelona = (
    [((40, 28), "Barcino", 100)],
    Civ.INDEPENDENT_2.value,
    1,
    Unit.ARCHER.value,
    1,
    -1,
    0,
)
tToulouse = (
    [((41, 34), "Tolosa", 30), ((40, 34), "Tolosa", 30), ((42, 32), "Narbo", 40)],
    Civ.BARBARIAN.value,
    1,
    Unit.ARCHER.value,
    0,
    -1,
    0,
)
tMarseilles = (
    [((46, 32), "Massilia", 50), ((46, 33), "Aquae Sextiae", 50)],
    Civ.INDEPENDENT.value,
    1,
    Unit.ARCHER.value,
    1,
    Religion.CATHOLICISM.value,
    0,
)
tNantes = (
    [((36, 43), "Naoned", 50), ((35, 43), "Gwened", 30), ((37, 44), "Roazhon", 20)],
    Civ.INDEPENDENT_2.value,
    1,
    Unit.ARCHER.value,
    1,
    -1,
    0,
)
tCaen = (
    [((40, 47), "Caen", 100)],
    Civ.INDEPENDENT_4.value,
    2,
    Unit.ARCHER.value,
    1,
    Religion.CATHOLICISM.value,
    1,
)
tLyon = (
    [((46, 37), "Lyon", 100)],
    Civ.INDEPENDENT_3.value,
    2,
    Unit.ARCHER.value,
    2,
    Religion.CATHOLICISM.value,
    1,
)
tTunis = ([((49, 17), "Tunis", 100)], Civ.INDEPENDENT_4.value, 2, Unit.ARCHER.value, 1, -1, 0)
tYork = ([((39, 59), "Eboracum", 100)], Civ.INDEPENDENT_4.value, 1, Unit.ARCHER.value, 2, -1, 1)
tLondon = (
    [((41, 52), "Londinium", 100)],
    Civ.INDEPENDENT.value,
    2,
    Unit.ARCHER.value,
    2,
    Religion.CATHOLICISM.value,
    0,
)
tMilan = (
    [((52, 37), "Mediolanum", 100)],
    Civ.INDEPENDENT.value,
    2,
    Unit.ARCHER.value,
    2,
    Religion.CATHOLICISM.value,
    0,
)
tFlorence = (
    [((54, 32), "Florentia", 40), ((53, 32), "Pisae", 40), ((57, 31), "Ankon", 20)],
    Civ.INDEPENDENT_2.value,
    2,
    Unit.ARCHER.value,
    2,
    Religion.CATHOLICISM.value,
    0,
)
tTripoli = ([((54, 8), "Tripoli", 100)], Civ.BARBARIAN.value, 1, Unit.ARCHER.value, 1, -1, 0)
tAugsburg = (
    [((55, 41), "Augsburg", 100)],
    Civ.INDEPENDENT_3.value,
    1,
    Unit.ARCHER.value,
    2,
    -1,
    0,
)
tNapoli = (
    [((59, 24), "Neapolis", 40), ((60, 25), "Beneventum", 40), ((62, 24), "Tarentum", 20)],
    Civ.INDEPENDENT.value,
    2,
    Unit.ARCHER.value,
    1,
    -1,
    0,
)
tRagusa = (
    [((64, 28), "Ragusa", 100)],
    Civ.INDEPENDENT_2.value,
    1,
    Unit.ARCHER.value,
    2,
    Religion.CATHOLICISM.value,
    0,
)
tSeville = ([((27, 21), "Hispalis", 100)], Civ.INDEPENDENT_4.value, 1, Unit.ARCHER.value, 2, -1, 0)
tPalermo = (
    [((55, 19), "Palermo", 60), ((58, 17), "Syracuse", 40)],
    Civ.INDEPENDENT_3.value,
    2,
    Unit.ARCHER.value,
    1,
    Religion.CATHOLICISM.value,
    1,
)
# 552 AD
tInverness = (
    [((37, 67), "Inbhir Nis", 50), ((37, 65), "Scaig", 50)],
    Civ.BARBARIAN.value,
    1,
    Unit.ARCHER.value,
    1,
    -1,
    0,
)  # reduced to town on spawn of Scotland
# 600 AD
tRhodes = (
    [((80, 13), "Rhodes", 100)],
    Civ.INDEPENDENT_2.value,
    1,
    Unit.ARCHER.value,
    1,
    Religion.ORTHODOXY.value,
    0,
)
# 640 AD
tNorwich = (
    [((43, 55), "Norwich", 100)],
    Civ.INDEPENDENT_3.value,
    1,
    Unit.ARCHER.value,
    1,
    -1,
    1,
)  # reduced to town on spawn of England
# 670 AD
tKairouan = (
    [((48, 14), "Kairouan", 100)],
    Civ.INDEPENDENT_2.value,
    1,
    Unit.ARCHER.value,
    1,
    Religion.ISLAM.value,
    0,
)
# 680 AD
tToledo = (
    [((30, 27), "Toledo", 100)],
    Civ.BARBARIAN.value,
    1,
    Unit.ARCHER.value,
    1,
    Religion.CATHOLICISM.value,
    1,
)
tLeicester = (
    [((39, 56), "Ligeraceaster", 100)],
    Civ.INDEPENDENT.value,
    1,
    Unit.ARCHER.value,
    1,
    -1,
    0,
)  # reduced to town on spawn of England
# 700 AD
tValencia = (
    [((36, 25), "Valencia", 100)],
    Civ.INDEPENDENT.value,
    1,
    Unit.ARCHER.value,
    1,
    Religion.CATHOLICISM.value,
    1,
)
tPamplona = (
    [((35, 32), "Pamplona", 70), ((34, 33), "Pamplona", 30)],
    Civ.INDEPENDENT_4.value,
    1,
    Unit.CROSSBOWMAN.value,
    2,
    -1,
    0,
)
tLubeck = (
    [((57, 54), "Liubice", 40), ((57, 53), "Liubice", 60)],
    Civ.INDEPENDENT_2.value,
    1,
    Unit.ARCHER.value,
    2,
    -1,
    1,
)
tPorto = (
    [((23, 31), "Portucale", 100)],
    Civ.INDEPENDENT_3.value,
    1,
    Unit.CROSSBOWMAN.value,
    2,
    Religion.CATHOLICISM.value,
    0,
)
tDublin = (
    [((32, 58), "Teamhair", 100)],
    Civ.BARBARIAN.value,
    1,
    Unit.SPEARMAN.value,
    1,
    Religion.CATHOLICISM.value,
    1,
)  # Hill of Tara, later becomes Dublin
tDownpatrick = (
    [((33, 61), "Rath Celtair", 20), ((29, 60), "Cruiachain", 30), ((29, 56), "Caisel", 50)],
    Civ.BARBARIAN.value,
    1,
    Unit.ARCHER.value,
    0,
    -1,
    1,
)  # Cruiachain = Rathcroghan, later becomes Sligo; Caisel = Cashel, later becomes Cork
# 760 AD
tTonsberg = (
    [((57, 65), "Tonsberg", 100)],
    Civ.INDEPENDENT_3.value,
    1,
    Unit.ARCHER.value,
    2,
    -1,
    0,
)
# 768 AD
tRaska = ([((68, 28), "Ras", 100)], Civ.INDEPENDENT_2.value, 1, Unit.ARCHER.value, 2, -1, 1)
# 780 AD
tFez = ([((29, 12), "Fes", 100)], Civ.INDEPENDENT_4.value, 1, Unit.CROSSBOWMAN.value, 2, -1, 1)
# 800 AD
tMilanR = (
    [((52, 37), "Milano", 100)],
    Civ.INDEPENDENT.value,
    4,
    Unit.ARCHER.value,
    2,
    Religion.CATHOLICISM.value,
    0,
)  # respawn, in case it was razed
# tFlorenceR = ( [ ((54, 32), "Firenze", 100) ], Civ.INDEPENDENT_2.value, 4, Unit.ARCHER.value, 2, Religion.CATHOLICISM.value, 0 ) #respawn, doesn't work with the multiple options in 500AD
tPrague = (
    [((60, 44), "Praha", 100)],
    Civ.INDEPENDENT.value,
    1,
    Unit.CROSSBOWMAN.value,
    2,
    Religion.CATHOLICISM.value,
    1,
)
tKursk = ([((90, 48), "Kursk", 100)], Civ.INDEPENDENT_4.value, 1, Unit.ARCHER.value, 2, -1, 0)
tCalais = (
    [((44, 50), "Calais", 50), ((45, 50), "Dunkerque", 50)],
    Civ.INDEPENDENT_3.value,
    1,
    Unit.CROSSBOWMAN.value,
    2,
    -1,
    0,
)
tNidaros = (
    [((57, 71), "Nidaros", 100)],
    Civ.INDEPENDENT_3.value,
    1,
    Unit.ARCHER.value,
    1,
    -1,
    1,
)  # Trondheim
tUppsala = (
    [((65, 66), "Uppsala", 100)],
    Civ.INDEPENDENT_4.value,
    1,
    Unit.ARCHER.value,
    2,
    -1,
    1,
)  # reduced to town on spawn of Sweden
tBeloozero = (
    [((87, 65), "Beloozero", 100)],
    Civ.INDEPENDENT_4.value,
    1,
    Unit.CROSSBOWMAN.value,
    1,
    -1,
    1,
)
tZagreb = (
    [((62, 34), "Sisak", 100)],
    Civ.INDEPENDENT.value,
    2,
    Unit.ARCHER.value,
    2,
    -1,
    0,
)  # many Slavic princes reigned from Sisak in the 9th century, great for gameplay (buffer zone between Venice and Hungary)
# 850 AD
tBrennabor = (
    [((59, 50), "Brennabor", 50), ((60, 50), "Brennabor", 50)],
    Civ.BARBARIAN.value,
    1,
    Unit.ARCHER.value,
    2,
    -1,
    0,
)  # Brandenburg or Berlin
# 860 AD
# tEdinburgh = ( [ ((37, 63), "Eidyn Dun", 100) ], Civ.BARBARIAN.value, 1, Unit.ARCHER.value, 1, -1, 0)
# 880 AD
tApulum = (
    [((73, 35), "Belograd", 80), ((73, 37), "Napoca", 20)],
    Civ.INDEPENDENT.value,
    1,
    Unit.ARCHER.value,
    2,
    -1,
    0,
)  # Gyulafehérvár or Kolozsvár
# 900 AD
tTvanksta = (
    [((69, 53), "Tvanksta", 100)],
    Civ.INDEPENDENT_4.value,
    1,
    Unit.CROSSBOWMAN.value,
    2,
    -1,
    0,
)  # Königsberg
tKrakow = (
    [((68, 44), "Krakow", 100)],
    Civ.INDEPENDENT_3.value,
    1,
    Unit.CROSSBOWMAN.value,
    2,
    Religion.CATHOLICISM.value,
    0,
)
tRiga = (
    [((74, 58), "Riga", 100)],
    Civ.INDEPENDENT.value,
    2,
    Unit.CROSSBOWMAN.value,
    2,
    -1,
    1,
)  # maybe call it Duna in the early pediod (Duna is the name of a sheltered natural harbor near Riga)
tWales = (
    [((36, 54), "Caerdydd", 50), ((35, 57), "Aberffraw", 50)],
    Civ.BARBARIAN.value,
    1,
    Unit.ARCHER.value,
    1,
    -1,
    1,
)  # Cardiff and Caernarfon
tVisby = (
    [((67, 60), "Visby", 100)],
    Civ.INDEPENDENT_2.value,
    1,
    Unit.CROSSBOWMAN.value,
    1,
    -1,
    0,
)  # used to spawn in 1393 in the old system
# 911 AD
tCaenR = (
    [((40, 47), "Caen", 100)],
    Civ.INDEPENDENT_2.value,
    1,
    Unit.CROSSBOWMAN.value,
    2,
    Religion.CATHOLICISM.value,
    0,
)  # respawn, on the establishment of the Duchy of Normandy
# 960 AD
tMinsk = ([((79, 52), "Minsk", 100)], Civ.INDEPENDENT_3.value, 1, Unit.CROSSBOWMAN.value, 2, -1, 0)
tSmolensk = (
    [((84, 55), "Smolensk", 100)],
    Civ.INDEPENDENT_4.value,
    1,
    Unit.CROSSBOWMAN.value,
    1,
    -1,
    0,
)
# 988 AD
tDublinR = (
    [((32, 58), "Dubh Linn", 100)],
    Civ.BARBARIAN.value,
    1,
    Unit.CROSSBOWMAN.value,
    1,
    Religion.CATHOLICISM.value,
    1,
)  # respawn, on the traditional Irish foundation date of Dublin
# 1010 AD
tYaroslavl = (
    [((92, 61), "Yaroslavl", 100)],
    Civ.INDEPENDENT_3.value,
    1,
    Unit.CROSSBOWMAN.value,
    1,
    -1,
    0,
)
# 1050 AD
tGroningen = (
    [((52, 54), "Groningen", 100)],
    Civ.INDEPENDENT_2.value,
    1,
    Unit.CROSSBOWMAN.value,
    2,
    Religion.CATHOLICISM.value,
    0,
)
tKalmar = (
    [((64, 60), "Kalmar", 100)],
    Civ.INDEPENDENT_2.value,
    2,
    Unit.CROSSBOWMAN.value,
    1,
    Religion.CATHOLICISM.value,
    1,
)
# 1060 AD
# tMus = ( [ ((99, 21), "Mus", 100) ], Civ.BARBARIAN.value, 1, Unit.SELJUK_CROSSBOW.value, 2, -1, 0) #out of the map, not that important to represent the Seljuk/Timurid invasions this way
# 1110 AD
tGraz = (
    [((61, 37), "Graz", 100)],
    Civ.INDEPENDENT_3.value,
    2,
    Unit.CROSSBOWMAN.value,
    2,
    Religion.CATHOLICISM.value,
    0,
)
# 1124 AD
tHalych = (
    [((77, 41), "Halych", 100)],
    Civ.INDEPENDENT_2.value,
    2,
    Unit.CROSSBOWMAN.value,
    2,
    Religion.ORTHODOXY.value,
    0,
)
# 1200 AD
tRigaR = (
    [((74, 58), "Riga", 100)],
    Civ.INDEPENDENT.value,
    3,
    Unit.CROSSBOWMAN.value,
    2,
    -1,
    1,
)  # respawn
# tSaraiBatu = ( [ ((99, 40), "Sarai Batu", 100) ], Civ.BARBARIAN.value, 1, Unit.MONGOL_KESHIK.value, 2, -1, 0) #out of the map, not that important to represent the Mongol invasions this way
# 1227 AD
tTripoliR = (
    [((54, 8), "Tarabulus", 100)],
    Civ.BARBARIAN.value,
    3,
    Unit.ARBALEST.value,
    2,
    Religion.ISLAM.value,
    1,
)  # respawn
# 1250 AD
tAbo = ([((71, 66), "Abo", 100)], Civ.INDEPENDENT_4.value, 1, Unit.CROSSBOWMAN.value, 1, -1, 0)
tPerekop = (
    [((87, 36), "Or Qapi", 100)],
    Civ.BARBARIAN.value,
    1,
    Unit.MONGOL_KESHIK.value,
    2,
    -1,
    0,
)
# 1320 AD
tNizhnyNovgorod = (
    [((97, 58), "Nizhny Novgorod", 100)],
    Civ.INDEPENDENT.value,
    1,
    Unit.CROSSBOWMAN.value,
    1,
    -1,
    0,
)
# 1392 AD
tTanais = (
    [((96, 38), "Tana", 100)],
    Civ.BARBARIAN.value,
    1,
    Unit.LONGBOWMAN.value,
    2,
    Religion.ISLAM.value,
    0,
)
# 1410 AD
tReykjavik = (
    [((2, 70), "Reykjavik", 100)],
    Civ.INDEPENDENT.value,
    1,
    Unit.VIKING_BERSERKER.value,
    2,
    -1,
    0,
)
# 1530 AD
tValletta = (
    [((57, 14), "Valletta", 100)],
    Civ.INDEPENDENT_4.value,
    1,
    Unit.KNIGHT_OF_ST_JOHNS.value,
    3,
    Religion.CATHOLICISM.value,
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
        tNapoli,
        tRagusa,
        tSeville,
        tPalermo,
    ],
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
        Province.SERBIA.value,
        [],
        [],
        [DateTurn.i508AD, DateTurn.i852AD, DateTurn.i1346AD],
        [20, 20, 20],
        [Unit.AXEMAN.value, Unit.AXEMAN.value, Unit.LONG_SWORDSMAN.value],
        [2, 1, 2],
        ["TXT_KEY_THE_SERBS", "TXT_KEY_SERBIAN"],
    ],
    [
        Province.SCOTLAND.value,
        [Civ.SCOTLAND.value],
        [],
        [DateTurn.i1297AD, DateTurn.i1569AD, DateTurn.i1715AD],
        [20, 10, 20],
        [Unit.HIGHLANDER.value, Unit.MUSKETMAN.value, Unit.GRENADIER.value],
        [2, 2, 2],
        ["TXT_KEY_THE_SCOTS", "TXT_KEY_SCOTTISH"],
    ],
    [
        Province.CATALONIA.value,
        [Civ.ARAGON.value],
        [],
        [DateTurn.i1164AD + 10, DateTurn.i1640AD],
        [20, 10],
        [Unit.LONG_SWORDSMAN.value, Unit.MUSKETMAN.value],
        [2, 2],
        ["TXT_KEY_THE_CATALANS", "TXT_KEY_CATALAN"],
    ],
    [
        Province.JERUSALEM.value,
        [Civ.ARABIA.value, Civ.OTTOMAN.value, Civ.BYZANTIUM.value],
        [
            Religion.ISLAM.value,
        ],
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
            Unit.MACEMAN.value,
            Unit.MACEMAN.value,
            Unit.MACEMAN.value,
            Unit.KNIGHT.value,
            Unit.KNIGHT.value,
            Unit.KNIGHT.value,
            Unit.KNIGHT.value,
            Unit.KNIGHT.value,
        ],
        [3, 3, 4, 3, 3, 3, 3, 3],
        ["TXT_KEY_THE_MUSLIMS", "TXT_KEY_MUSLIM"],
    ],
    [
        Province.SYRIA.value,
        [Civ.ARABIA.value, Civ.OTTOMAN.value, Civ.BYZANTIUM.value],
        [
            Religion.ISLAM.value,
        ],
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
            Unit.MACEMAN.value,
            Unit.MACEMAN.value,
            Unit.MACEMAN.value,
            Unit.KNIGHT.value,
            Unit.KNIGHT.value,
            Unit.KNIGHT.value,
            Unit.KNIGHT.value,
            Unit.KNIGHT.value,
        ],
        [3, 3, 4, 3, 3, 3, 3, 3],
        ["TXT_KEY_THE_MUSLIMS", "TXT_KEY_MUSLIM"],
    ],
    [
        Province.ORAN.value,
        [],
        [],
        [DateTurn.i1236AD, DateTurn.i1346AD, DateTurn.i1359AD, DateTurn.i1542AD],
        [40, 10, 10, 20],
        [
            Unit.KNIGHT.value,
            Unit.HEAVY_LANCER.value,
            Unit.HEAVY_LANCER.value,
            Unit.MUSKETMAN.value,
        ],
        [2, 2, 2, 2],
        ["TXT_KEY_THE_ZIYYANIDS", "TXT_KEY_ZIYYANID"],
    ],
    [
        Province.FEZ.value,
        [Civ.MOROCCO.value],
        [],
        [DateTurn.i1473AD],
        [30],
        [Unit.ARQUEBUSIER.value],
        [4],
        ["TXT_KEY_THE_WATTASIDS", "TXT_KEY_WATTASID"],
    ],
]
# 3Miro: Jerusalem and Syria were added here, so the Crusaders will not be able to control it for too long


class Barbs:
    def getRevolDates(self):
        return sd.scriptDict["lNextMinorRevolt"]

    def setRevolDates(self, lNextMinorRevolt):
        sd.scriptDict["lNextMinorRevolt"] = lNextMinorRevolt

    def getTempFlippingCity(self):
        return sd.scriptDict["tempFlippingCity"]

    def setTempFlippingCity(self, tNewValue):
        sd.scriptDict["tempFlippingCity"] = tNewValue

    def getNationRevoltIndex(self):
        return sd.scriptDict["lRevoltinNationRevoltIndex"]

    def setNationRevoltIndex(self, iNationIndex, iRevoltIndex):
        sd.scriptDict["lRevoltinNationRevoltIndex"] = [iNationIndex, iRevoltIndex]

    def makeUnit(self, iUnit, iPlayer, tCoords, iNum, iForceAttack, szName):
        "Makes iNum units for player iPlayer of the type iUnit at tCoords."
        for i in range(iNum):
            player = gc.getPlayer(iPlayer)
            if iForceAttack == 0:
                pUnit = player.initUnit(
                    iUnit,
                    tCoords[0],
                    tCoords[1],
                    UnitAITypes.NO_UNITAI,
                    DirectionTypes.DIRECTION_SOUTH,
                )
            elif iForceAttack == 1:
                pUnit = player.initUnit(
                    iUnit,
                    tCoords[0],
                    tCoords[1],
                    UnitAITypes.UNITAI_ATTACK,
                    DirectionTypes.DIRECTION_SOUTH,
                )
            elif iForceAttack == 2:
                pUnit = player.initUnit(
                    iUnit,
                    tCoords[0],
                    tCoords[1],
                    UnitAITypes.UNITAI_ATTACK_SEA,
                    DirectionTypes.DIRECTION_SOUTH,
                )
            if szName != "":
                pUnit.setName(szName)

    def checkTurn(self, iGameTurn):
        # Handicap level modifier
        iHandicap = gc.getGame().getHandicapType() - 1
        # gc.getGame().getHandicapType: Viceroy=0, Monarch=1, Emperor=2
        # iHandicap: Viceroy=-1, Monarch=0, Emperor=1

        # The Human player usually gets some additional barbarians
        iHuman = human()

        # Mediterranean Pirates (Light before 1500, then heavy for rest of game)
        if DateTurn.i960AD <= iGameTurn < DateTurn.i1401AD:
            self.spawnPirate(
                Civ.BARBARIAN.value,
                (9, 15),
                (55, 33),
                Unit.WAR_GALLEY.value,
                2,
                0,
                0,
                iGameTurn,
                10,
                3,
                utils.outerSeaSpawn,
                1,
                "",
            )
        elif iGameTurn >= DateTurn.i1401AD:
            self.spawnPirate(
                Civ.BARBARIAN.value,
                (9, 15),
                (55, 33),
                Unit.CORSAIR.value,
                2,
                0,
                0,
                iGameTurn,
                10,
                3,
                utils.outerSeaSpawn,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_BARBARY_PIRATES", ()),
            )
            # extra Corsairs around Tunisia
            self.spawnPirate(
                Civ.BARBARIAN.value,
                (42, 15),
                (54, 23),
                Unit.CORSAIR.value,
                1,
                0,
                0,
                iGameTurn,
                5,
                0,
                utils.outerSeaSpawn,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_BARBARY_PIRATES", ()),
            )
        if DateTurn.i1200AD <= iGameTurn < DateTurn.i1500AD:
            self.spawnPirate(
                Civ.BARBARIAN.value,
                (9, 15),
                (55, 33),
                Unit.COGGE.value,
                1,
                Unit.SWORDSMAN.value,
                2,
                iGameTurn,
                10,
                5,
                utils.outerSeaSpawn,
                1,
                "",
            )
        elif iGameTurn >= DateTurn.i1500AD:
            self.spawnPirate(
                Civ.BARBARIAN.value,
                (9, 15),
                (55, 33),
                Unit.GALLEON.value,
                1,
                Unit.MUSKETMAN.value,
                2,
                iGameTurn,
                10,
                5,
                utils.outerSeaSpawn,
                1,
                "",
            )

        # Germanic Barbarians throughout Western Europe (France, Germany)
        if iGameTurn < DateTurn.i600AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (43, 42),
                (50, 50),
                Unit.AXEMAN.value,
                1,
                iGameTurn,
                11,
                1,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()),
            )
            if Civ.FRANCE.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (42, 40),
                    (56, 48),
                    Unit.AXEMAN.value,
                    1,
                    iGameTurn,
                    9,
                    3,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (45, 45),
                    (60, 55),
                    Unit.SPEARMAN.value,
                    1,
                    iGameTurn,
                    18,
                    7,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()),
                )
        elif DateTurn.i600AD <= iGameTurn < DateTurn.i800AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (43, 42),
                (50, 50),
                Unit.AXEMAN.value,
                1,
                iGameTurn,
                9,
                2,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (42, 40),
                (56, 48),
                Unit.AXEMAN.value,
                1,
                iGameTurn,
                11,
                4,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()),
            )
            if Civ.FRANCE.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (43, 42),
                    (50, 50),
                    Unit.AXEMAN.value,
                    1,
                    iGameTurn,
                    9,
                    3,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (45, 45),
                    (60, 55),
                    Unit.SPEARMAN.value,
                    1 + iHandicap,
                    iGameTurn,
                    11,
                    4,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (46, 48),
                    (62, 55),
                    Unit.AXEMAN.value,
                    1 + iHandicap,
                    iGameTurn,
                    14,
                    9,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_GERMANIC_TRIBES", ()),
                )

        # Longobards in Italy
        if DateTurn.i632AD <= iGameTurn <= DateTurn.i800AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (49, 33),
                (53, 36),
                Unit.AXEMAN.value,
                1 + iHandicap,
                iGameTurn,
                10,
                3,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_LONGOBARDS", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (49, 33),
                (53, 36),
                Unit.SPEARMAN.value,
                1,
                iGameTurn,
                12,
                0,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_LONGOBARDS", ()),
            )

        # Visigoths in Iberia
        if DateTurn.i712AD <= iGameTurn <= DateTurn.i892AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (22, 21),
                (26, 25),
                Unit.AXEMAN.value,
                1,
                iGameTurn,
                7,
                0,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_VISIGOTHS", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (23, 23),
                (27, 28),
                Unit.SPEARMAN.value,
                1,
                iGameTurn,
                7,
                3,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_VISIGOTHS", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (26, 27),
                (31, 32),
                Unit.MOUNTED_INFANTRY.value,
                1,
                iGameTurn,
                9,
                5,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_VISIGOTHS", ()),
            )
            if Civ.CORDOBA.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (24, 31),
                    (27, 34),
                    Unit.AXEMAN.value,
                    1 + iHandicap,
                    iGameTurn,
                    7,
                    0,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_VISIGOTHS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (27, 28),
                    (31, 36),
                    Unit.MOUNTED_INFANTRY.value,
                    1,
                    iGameTurn,
                    6,
                    3,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_VISIGOTHS", ()),
                )

        # Berbers in North Africa
        if DateTurn.i700AD <= iGameTurn < DateTurn.i1020AD:
            # Tunesia
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (28, 10),
                (35, 14),
                Unit.HORSE_ARCHER.value,
                1 + iHandicap,
                iGameTurn,
                8,
                0,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_BERBERS", ()),
            )
            # Morocco
            if Civ.CORDOBA.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (21, 3),
                    (27, 12),
                    Unit.HORSE_ARCHER.value,
                    1,
                    iGameTurn,
                    9,
                    0,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_BERBERS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (22, 3),
                    (27, 10),
                    Unit.AXEMAN.value,
                    1,
                    iGameTurn,
                    11,
                    5,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_BERBERS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (23, 3),
                    (27, 8),
                    Unit.SPEARMAN.value,
                    1,
                    iGameTurn,
                    7,
                    3,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_BERBERS", ()),
                )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (22, 3),
                    (27, 10),
                    Unit.AXEMAN.value,
                    1,
                    iGameTurn,
                    14,
                    5,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_BERBERS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (23, 3),
                    (27, 8),
                    Unit.SPEARMAN.value,
                    1,
                    iGameTurn,
                    8,
                    3,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_BERBERS", ()),
                )

        # Avars in the Carpathian Basin
        if DateTurn.i632AD <= iGameTurn < DateTurn.i800AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (60, 30),
                (75, 40),
                Unit.HORSE_ARCHER.value,
                1,
                iGameTurn,
                5,
                0,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_AVARS", ()),
            )
            if Civ.BULGARIA.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (66, 26),
                    (73, 29),
                    Unit.HORSE_ARCHER.value,
                    1 + iHandicap,
                    iGameTurn,
                    6,
                    1,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_AVARS", ()),
                )

        # Early barbs for Byzantium:
        if iGameTurn < DateTurn.i640AD:
            # Pre-Bulgarian Slavs in the Balkans
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (68, 18),
                (78, 28),
                Unit.AXEMAN.value,
                1,
                iGameTurn,
                8,
                0,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_SOUTHERN_SLAVS", ()),
            )
            if Civ.BYZANTIUM.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (64, 21),
                    (75, 25),
                    Unit.AXEMAN.value,
                    1 + iHandicap,
                    iGameTurn,
                    11,
                    3,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SOUTHERN_SLAVS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (68, 18),
                    (78, 28),
                    Unit.SPEARMAN.value,
                    1,
                    iGameTurn,
                    8,
                    0,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SOUTHERN_SLAVS", ()),
                )
            # Sassanids in Anatolia
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (90, 15),
                (99, 28),
                Unit.LANCER.value,
                1,
                iGameTurn,
                6,
                2,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_SASSANIDS", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (94, 19),
                (98, 26),
                Unit.LANCER.value,
                1,
                iGameTurn,
                9,
                1,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_SASSANIDS", ()),
            )
            if Civ.BYZANTIUM.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (90, 15),
                    (99, 28),
                    Unit.LANCER.value,
                    1,
                    iGameTurn,
                    6,
                    2,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SASSANIDS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (94, 19),
                    (98, 26),
                    Unit.LANCER.value,
                    1 + iHandicap,
                    iGameTurn,
                    9,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SASSANIDS", ()),
                )
        # Barbs in NW Greece
        if iGameTurn < DateTurn.i720AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (66, 21),
                (69, 28),
                Unit.AXEMAN.value,
                1,
                iGameTurn,
                9,
                3,
                utils.outerInvasion,
                1,
                "",
            )
            if Civ.BYZANTIUM.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (66, 21),
                    (69, 28),
                    Unit.SPEARMAN.value,
                    1 + iHandicap,
                    iGameTurn,
                    9,
                    3,
                    utils.outerInvasion,
                    1,
                    "",
                )

        # Serbs in the Southern Balkans
        if DateTurn.i1025AD <= iGameTurn < DateTurn.i1282AD:
            if Civ.BYZANTIUM.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (67, 24),
                    (73, 28),
                    Unit.AXEMAN.value,
                    1,
                    iGameTurn,
                    9,
                    3,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SERBS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (67, 24),
                    (73, 28),
                    Unit.LANCER.value,
                    1 + iHandicap,
                    iGameTurn,
                    11,
                    7,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SERBS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (69, 25),
                    (71, 29),
                    Unit.SWORDSMAN.value,
                    1,
                    iGameTurn,
                    7,
                    4,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SERBS", ()),
                )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (67, 24),
                    (73, 28),
                    Unit.AXEMAN.value,
                    1,
                    iGameTurn,
                    9,
                    3,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SERBS", ()),
                )

        # Khazars
        if DateTurn.i660AD <= iGameTurn < DateTurn.i864AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (88, 31),
                (99, 40),
                Unit.AXEMAN.value,
                1,
                iGameTurn,
                8,
                0,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_KHAZARS", ()),
            )
        elif DateTurn.i864AD <= iGameTurn < DateTurn.i920AD:
            if Civ.KIEV.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (88, 31),
                    (99, 40),
                    Unit.AXEMAN.value,
                    1,
                    iGameTurn,
                    7,
                    2,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_KHAZARS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (88, 31),
                    (99, 40),
                    Unit.SPEARMAN.value,
                    1,
                    iGameTurn,
                    5,
                    2,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_KHAZARS", ()),
                )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (88, 31),
                    (99, 40),
                    Unit.AXEMAN.value,
                    1,
                    iGameTurn,
                    11,
                    2,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_KHAZARS", ()),
                )

        # Pechenegs
        if DateTurn.i920AD <= iGameTurn < DateTurn.i1040AD:
            # in the Rus
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (89, 34),
                (97, 40),
                Unit.STEPPE_HORSE_ARCHER.value,
                1,
                iGameTurn,
                8,
                3,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_PECHENEGS", ()),
            )
            if Civ.KIEV.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (91, 35),
                    (99, 44),
                    Unit.STEPPE_HORSE_ARCHER.value,
                    1 + iHandicap,
                    iGameTurn,
                    5,
                    1,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_PECHENEGS", ()),
                )
            # in Hungary
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (66, 35),
                (75, 42),
                Unit.STEPPE_HORSE_ARCHER.value,
                1,
                iGameTurn,
                9,
                1,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_PECHENEGS", ()),
            )
            if Civ.HUNGARY.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (66, 35),
                    (75, 42),
                    Unit.STEPPE_HORSE_ARCHER.value,
                    1 + iHandicap,
                    iGameTurn,
                    9,
                    1,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_PECHENEGS", ()),
                )
            # in Bulgaria
            elif Civ.BULGARIA.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (77, 31),
                    (79, 33),
                    Unit.STEPPE_HORSE_ARCHER.value,
                    2 + iHandicap,
                    iGameTurn,
                    5,
                    1,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_PECHENEGS", ()),
                )

        # Cumans and Kipchaks
        elif DateTurn.i1040AD <= iGameTurn < DateTurn.i1200AD:
            # in the Rus
            if Civ.KIEV.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (89, 34),
                    (99, 40),
                    Unit.STEPPE_HORSE_ARCHER.value,
                    2,
                    iGameTurn,
                    7,
                    5,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_CUMANS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (90, 33),
                    (97, 44),
                    Unit.STEPPE_HORSE_ARCHER.value,
                    2 + iHandicap,
                    iGameTurn,
                    9,
                    1,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_KIPCHAKS", ()),
                )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (89, 34),
                    (99, 40),
                    Unit.STEPPE_HORSE_ARCHER.value,
                    1,
                    iGameTurn,
                    7,
                    5,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_CUMANS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (90, 33),
                    (97, 44),
                    Unit.STEPPE_HORSE_ARCHER.value,
                    1,
                    iGameTurn,
                    9,
                    1,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_KIPCHAKS", ()),
                )
            # in Hungary
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (64, 33),
                (77, 43),
                Unit.STEPPE_HORSE_ARCHER.value,
                1,
                iGameTurn,
                7,
                1,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_CUMANS", ()),
            )
            if Civ.HUNGARY.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (64, 33),
                    (77, 43),
                    Unit.STEPPE_HORSE_ARCHER.value,
                    1,
                    iGameTurn,
                    7,
                    1,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_CUMANS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (66, 35),
                    (75, 42),
                    Unit.STEPPE_HORSE_ARCHER.value,
                    1,
                    iGameTurn,
                    9,
                    4,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_KIPCHAKS", ()),
                )
            # in Bulgaria
            if Civ.BULGARIA.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (78, 32),
                    (80, 34),
                    Unit.STEPPE_HORSE_ARCHER.value,
                    1,
                    iGameTurn,
                    7,
                    3,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_CUMANS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (78, 32),
                    (80, 34),
                    Unit.STEPPE_HORSE_ARCHER.value,
                    1,
                    iGameTurn,
                    7,
                    3,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_KIPCHAKS", ()),
                )

        # Vikings on ships
        if Civ.NORWAY.value == iHuman:  # Humans can properly go viking without help
            pass
        elif DateTurn.i780AD <= iGameTurn < DateTurn.i1000AD:
            if Civ.FRANCE.value == iHuman:
                self.spawnVikings(
                    Civ.BARBARIAN.value,
                    (37, 48),
                    (50, 54),
                    Unit.VIKING_BERSERKER.value,
                    2,
                    iGameTurn,
                    8,
                    0,
                    utils.outerSeaSpawn,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_VIKINGS", ()),
                )
            else:
                self.spawnVikings(
                    Civ.BARBARIAN.value,
                    (37, 48),
                    (50, 54),
                    Unit.VIKING_BERSERKER.value,
                    1,
                    iGameTurn,
                    8,
                    0,
                    utils.outerSeaSpawn,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_VIKINGS", ()),
                )

        # Swedish Crusades
        elif DateTurn.i1150AD <= iGameTurn < DateTurn.i1210AD:
            self.spawnVikings(
                Civ.BARBARIAN.value,
                (71, 62),
                (76, 65),
                Unit.VIKING_BERSERKER.value,
                2,
                iGameTurn,
                6,
                1,
                utils.outerSeaSpawn,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_SWEDES", ()),
            )

        # Chudes in Finland and Estonia
        if DateTurn.i864AD <= iGameTurn < DateTurn.i1150AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (72, 67),
                (81, 72),
                Unit.AXEMAN.value,
                1,
                iGameTurn,
                7,
                0,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_CHUDES", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (74, 60),
                (76, 63),
                Unit.AXEMAN.value,
                1,
                iGameTurn,
                11,
                3,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_CHUDES", ()),
            )

        # Livonian Order as barbs in the area before the Prussian spawn, but only if Prussia is AI (no need for potentially gained extra units for the human player)
        # Also pre-Lithanian barbs for human Prussia a couple turns before the Lithuanian spawn
        if Civ.PRUSSIA.value == iHuman:
            if DateTurn.i1224AD <= iGameTurn < DateTurn.i1236AD:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (73, 56),
                    (76, 61),
                    Unit.AXEMAN.value,
                    1,
                    iGameTurn,
                    2,
                    1,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_BALTICS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (72, 54),
                    (75, 59),
                    Unit.AXEMAN.value,
                    1,
                    iGameTurn,
                    2,
                    1,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_BALTICS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (73, 56),
                    (76, 61),
                    Unit.HORSE_ARCHER.value,
                    1 + iHandicap,
                    iGameTurn,
                    2,
                    1,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_BALTICS", ()),
                )
        elif DateTurn.i1200AD <= iGameTurn < DateTurn.i1224AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (73, 57),
                (76, 61),
                Unit.TEUTONIC.value,
                1,
                iGameTurn,
                4,
                3,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_SWORD_BRETHEN", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (73, 57),
                (76, 61),
                Unit.SWORDSMAN.value,
                1,
                iGameTurn,
                4,
                1,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_SWORD_BRETHEN", ()),
            )

        # Couple melee barb units in Ireland:
        if DateTurn.i800AD <= iGameTurn < DateTurn.i900AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (28, 56),
                (33, 62),
                Unit.AXEMAN.value,
                1,
                iGameTurn,
                7,
                3,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_IRISH", ()),
            )

        # Anglo-Saxons before the Danish 1st UHV (Conquer England)
        elif DateTurn.i970AD <= iGameTurn < DateTurn.i1050AD:
            if Civ.DENMARK.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (36, 53),
                    (41, 59),
                    Unit.AXEMAN.value,
                    1,
                    iGameTurn,
                    8,
                    5,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_ANGLO_SAXONS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (33, 48),
                    (38, 54),
                    Unit.AXEMAN.value,
                    1,
                    iGameTurn,
                    5,
                    2,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_ANGLO_SAXONS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (33, 48),
                    (38, 54),
                    Unit.SWORDSMAN.value,
                    1,
                    iGameTurn,
                    11,
                    6,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_ANGLO_SAXONS", ()),
                )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (33, 48),
                    (38, 54),
                    Unit.AXEMAN.value,
                    1,
                    iGameTurn,
                    5,
                    2,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_ANGLO_SAXONS", ()),
                )

        # Scots to keep England busy, but only if Scotland is dead
        if not gc.getPlayer(Civ.SCOTLAND.value).isAlive():
            if DateTurn.i1060AD <= iGameTurn < DateTurn.i1320AD:
                if Civ.ENGLAND.value == iHuman:
                    self.spawnUnits(
                        Civ.BARBARIAN.value,
                        (39, 62),
                        (44, 66),
                        Unit.HIGHLANDER.value,
                        2,
                        iGameTurn,
                        11,
                        0,
                        utils.forcedInvasion,
                        1,
                        localText.getText("TXT_KEY_BARBARIAN_NAMES_SCOTS", ()),
                    )
                else:
                    self.spawnUnits(
                        Civ.BARBARIAN.value,
                        (39, 62),
                        (44, 66),
                        Unit.HIGHLANDER.value,
                        1,
                        iGameTurn,
                        11,
                        0,
                        utils.forcedInvasion,
                        1,
                        localText.getText("TXT_KEY_BARBARIAN_NAMES_SCOTS", ()),
                    )
            elif DateTurn.i1320AD <= iGameTurn < DateTurn.i1500AD:
                if Civ.ENGLAND.value == iHuman:
                    self.spawnUnits(
                        Civ.BARBARIAN.value,
                        (39, 62),
                        (44, 66),
                        Unit.HIGHLANDER.value,
                        2,
                        iGameTurn,
                        9,
                        0,
                        utils.forcedInvasion,
                        1,
                        localText.getText("TXT_KEY_BARBARIAN_NAMES_SCOTS", ()),
                    )
                    self.spawnUnits(
                        Civ.BARBARIAN.value,
                        (39, 64),
                        (44, 67),
                        Unit.HIGHLANDER.value,
                        2 + iHandicap,
                        iGameTurn,
                        17,
                        4,
                        utils.forcedInvasion,
                        1,
                        localText.getText("TXT_KEY_BARBARIAN_NAMES_SCOTS", ()),
                    )
                else:
                    self.spawnUnits(
                        Civ.BARBARIAN.value,
                        (39, 64),
                        (44, 67),
                        Unit.HIGHLANDER.value,
                        2,
                        iGameTurn,
                        17,
                        4,
                        utils.forcedInvasion,
                        1,
                        localText.getText("TXT_KEY_BARBARIAN_NAMES_SCOTS", ()),
                    )

        # Welsh in Britain
        if DateTurn.i1060AD <= iGameTurn < DateTurn.i1160AD:
            if Civ.ENGLAND.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (37, 53),
                    (39, 57),
                    Unit.WELSH_LONGBOWMAN.value,
                    1,
                    iGameTurn,
                    7,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_WELSH", ()),
                )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (37, 53),
                    (39, 57),
                    Unit.WELSH_LONGBOWMAN.value,
                    1,
                    iGameTurn,
                    13,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_WELSH", ()),
                )
        elif DateTurn.i1160AD <= iGameTurn < DateTurn.i1452AD:
            if Civ.ENGLAND.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (37, 53),
                    (39, 57),
                    Unit.WELSH_LONGBOWMAN.value,
                    2 + iHandicap,
                    iGameTurn,
                    12,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_WELSH", ()),
                )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (37, 53),
                    (39, 57),
                    Unit.WELSH_LONGBOWMAN.value,
                    1,
                    iGameTurn,
                    9,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_WELSH", ()),
                )

        # Magyars (preceeding Hungary)
        if DateTurn.i840AD <= iGameTurn < DateTurn.i892AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (54, 38),
                (61, 45),
                Unit.HORSE_ARCHER.value,
                1,
                iGameTurn,
                4,
                1,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_MAGYARS", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (66, 26),
                (73, 29),
                Unit.HORSE_ARCHER.value,
                1,
                iGameTurn,
                4,
                2,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_MAGYARS", ()),
            )
            if Civ.BULGARIA.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (77, 31),
                    (80, 34),
                    Unit.HORSE_ARCHER.value,
                    2 + iHandicap,
                    iGameTurn,
                    5,
                    0,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_MAGYARS", ()),
                )
            elif Civ.GERMANY.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (54, 38),
                    (61, 45),
                    Unit.HORSE_ARCHER.value,
                    2 + iHandicap,
                    iGameTurn,
                    5,
                    3,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_MAGYARS", ()),
                )

        # Wends in NE Germany
        if DateTurn.i860AD <= iGameTurn < DateTurn.i1053AD:
            if Civ.GERMANY.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (55, 49),
                    (60, 56),
                    Unit.AXEMAN.value,
                    1,
                    iGameTurn,
                    6,
                    1,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_WENDS", ()),
                )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (55, 49),
                    (60, 56),
                    Unit.AXEMAN.value,
                    1,
                    iGameTurn,
                    8,
                    1,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_WENDS", ()),
                )

        # Great Slav Rising in 983AD
        if (DateTurn.i983AD - 1) <= iGameTurn < (DateTurn.i983AD + 1):
            if Civ.GERMANY.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (53, 48),
                    (59, 55),
                    Unit.AXEMAN.value,
                    2,
                    iGameTurn,
                    2,
                    0,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_WENDS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (53, 48),
                    (59, 55),
                    Unit.SPEARMAN.value,
                    1,
                    iGameTurn,
                    2,
                    0,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_WENDS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (53, 48),
                    (59, 55),
                    Unit.SWORDSMAN.value,
                    1,
                    iGameTurn,
                    2,
                    0,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_WENDS", ()),
                )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (53, 48),
                    (59, 55),
                    Unit.AXEMAN.value,
                    1,
                    iGameTurn,
                    2,
                    0,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_WENDS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (53, 48),
                    (59, 55),
                    Unit.SPEARMAN.value,
                    1,
                    iGameTurn,
                    2,
                    0,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_WENDS", ()),
                )

        # Barbs in the middle east
        if DateTurn.i700AD <= iGameTurn <= DateTurn.i1300AD:
            if not gc.getTeam(gc.getPlayer(Civ.ARABIA.value).getTeam()).isHasTech(
                Technology.FARRIERS.value
            ):
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (94, 0),
                    (99, 3),
                    Unit.HORSE_ARCHER.value,
                    1,
                    iGameTurn,
                    11,
                    3,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_BEDUINS", ()),
                )
                if gc.getPlayer(Civ.ARABIA.value).isHuman():
                    self.spawnUnits(
                        Civ.BARBARIAN.value,
                        (94, 0),
                        (99, 3),
                        Unit.HORSE_ARCHER.value,
                        1 + iHandicap,
                        iGameTurn,
                        11,
                        3,
                        utils.outerInvasion,
                        1,
                        localText.getText("TXT_KEY_BARBARIAN_NAMES_BEDUINS", ()),
                    )
                    self.spawnUnits(
                        Civ.BARBARIAN.value,
                        (92, 1),
                        (98, 4),
                        Unit.HORSE_ARCHER.value,
                        1,
                        iGameTurn,
                        8,
                        1,
                        utils.forcedInvasion,
                        1,
                        localText.getText("TXT_KEY_BARBARIAN_NAMES_BEDUINS", ()),
                    )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (94, 0),
                    (99, 3),
                    Unit.BEDOUIN.value,
                    1,
                    iGameTurn,
                    10,
                    2,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_BEDUINS", ()),
                )
                if gc.getPlayer(Civ.ARABIA.value).isHuman():
                    self.spawnUnits(
                        Civ.BARBARIAN.value,
                        (94, 0),
                        (99, 3),
                        Unit.BEDOUIN.value,
                        1 + iHandicap,
                        iGameTurn,
                        10,
                        2,
                        utils.outerInvasion,
                        1,
                        localText.getText("TXT_KEY_BARBARIAN_NAMES_BEDUINS", ()),
                    )
                    self.spawnUnits(
                        Civ.BARBARIAN.value,
                        (95, 1),
                        (98, 5),
                        Unit.BEDOUIN.value,
                        1,
                        iGameTurn,
                        7,
                        3,
                        utils.forcedInvasion,
                        1,
                        localText.getText("TXT_KEY_BARBARIAN_NAMES_BEDUINS", ()),
                    )

        # Banu Hilal and Bani Hassan, in Morocco and Tunesia
        if DateTurn.i1040AD <= iGameTurn < DateTurn.i1229AD:
            if Civ.MOROCCO.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (40, 10),
                    (44, 14),
                    Unit.BEDOUIN.value,
                    2 + iHandicap,
                    iGameTurn,
                    11,
                    2,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_BANU_HILAL", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (44, 1),
                    (50, 8),
                    Unit.TOUAREG.value,
                    2 + iHandicap,
                    iGameTurn,
                    8,
                    5,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_BANU_HILAL", ()),
                )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (40, 10),
                    (44, 14),
                    Unit.BEDOUIN.value,
                    1,
                    iGameTurn,
                    11,
                    2,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_BANU_HILAL", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (44, 1),
                    (50, 8),
                    Unit.TOUAREG.value,
                    1,
                    iGameTurn,
                    8,
                    5,
                    utils.outerInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_BANU_HILAL", ()),
                )
        if DateTurn.i1640AD <= iGameTurn < DateTurn.i1680AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (18, 1),
                (22, 3),
                Unit.BEDOUIN.value,
                5 + iHandicap * 2,
                iGameTurn,
                3,
                1,
                utils.outerInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_BANI_HASSAN", ()),
            )

        # Pre Mongols to keep Kiev busy
        if DateTurn.i900AD <= iGameTurn < DateTurn.i1020AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (93, 35),
                (99, 44),
                Unit.HORSE_ARCHER.value,
                1,
                iGameTurn,
                13,
                1,
                utils.outerInvasion,
                1,
                "",
            )
        elif DateTurn.i1020AD <= iGameTurn < DateTurn.i1236AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (93, 35),
                (99, 44),
                Unit.HORSE_ARCHER.value,
                1,
                iGameTurn,
                9,
                5,
                utils.outerInvasion,
                1,
                "",
            )
            if Civ.KIEV.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (94, 32),
                    (97, 39),
                    Unit.HORSE_ARCHER.value,
                    2 + iHandicap,
                    iGameTurn,
                    10,
                    1,
                    utils.outerInvasion,
                    1,
                    "",
                )

        # Barbs in Anatolia pre Seljuks (but after Sassanids)
        if DateTurn.i700AD <= iGameTurn < DateTurn.i1050AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (97, 20),
                (99, 26),
                Unit.HORSE_ARCHER.value,
                1,
                iGameTurn,
                10,
                1,
                utils.outerInvasion,
                1,
                "",
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (95, 20),
                (99, 24),
                Unit.AXEMAN.value,
                1,
                iGameTurn,
                14,
                2,
                utils.outerInvasion,
                1,
                "",
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (95, 22),
                (97, 26),
                Unit.SPEARMAN.value,
                1,
                iGameTurn,
                16,
                6,
                utils.outerInvasion,
                1,
                "",
            )
            if Civ.BYZANTIUM.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (97, 20),
                    (99, 26),
                    Unit.HORSE_ARCHER.value,
                    1 + iHandicap,
                    iGameTurn,
                    10,
                    1,
                    utils.outerInvasion,
                    1,
                    "",
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (95, 20),
                    (99, 24),
                    Unit.AXEMAN.value,
                    1,
                    iGameTurn,
                    14,
                    2,
                    utils.outerInvasion,
                    1,
                    "",
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (95, 20),
                    (99, 24),
                    Unit.HORSE_ARCHER.value,
                    1 + iHandicap,
                    iGameTurn,
                    14,
                    2,
                    utils.outerInvasion,
                    1,
                    "",
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (95, 22),
                    (97, 26),
                    Unit.SPEARMAN.value,
                    1,
                    iGameTurn,
                    16,
                    6,
                    utils.outerInvasion,
                    1,
                    "",
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (95, 22),
                    (97, 26),
                    Unit.HORSE_ARCHER.value,
                    1 + iHandicap,
                    iGameTurn,
                    16,
                    6,
                    utils.outerInvasion,
                    1,
                    "",
                )

        # Seljuks
        if DateTurn.i1064AD <= iGameTurn < DateTurn.i1094AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (90, 21),
                (99, 28),
                Unit.SELJUK_LANCER.value,
                3,
                iGameTurn,
                3,
                0,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (90, 21),
                (99, 28),
                Unit.TURCOMAN_HORSE_ARCHER.value,
                1,
                iGameTurn,
                3,
                0,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (90, 21),
                (99, 28),
                Unit.SELJUK_CROSSBOW.value,
                1,
                iGameTurn,
                3,
                0,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (90, 21),
                (99, 28),
                Unit.SELJUK_SWORDSMAN.value,
                1,
                iGameTurn,
                3,
                0,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (92, 20),
                (99, 25),
                Unit.SELJUK_LANCER.value,
                3,
                iGameTurn,
                3,
                1,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (92, 20),
                (99, 25),
                Unit.TURCOMAN_HORSE_ARCHER.value,
                1,
                iGameTurn,
                3,
                1,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (92, 20),
                (99, 25),
                Unit.SELJUK_GUISARME.value,
                1,
                iGameTurn,
                3,
                1,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (92, 20),
                (99, 25),
                Unit.SELJUK_FOOTMAN.value,
                1,
                iGameTurn,
                3,
                1,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (95, 8),
                (99, 12),
                Unit.SELJUK_LANCER.value,
                2,
                iGameTurn,
                4,
                1,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (95, 8),
                (99, 12),
                Unit.SELJUK_CROSSBOW.value,
                1,
                iGameTurn,
                4,
                1,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
            )
            if Civ.BYZANTIUM.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (90, 21),
                    (99, 28),
                    Unit.SELJUK_LANCER.value,
                    1,
                    iGameTurn,
                    3,
                    0,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (90, 21),
                    (99, 28),
                    Unit.TURCOMAN_HORSE_ARCHER.value,
                    1,
                    iGameTurn,
                    3,
                    0,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (90, 21),
                    (99, 28),
                    Unit.SELJUK_CROSSBOW.value,
                    1 + iHandicap,
                    iGameTurn,
                    3,
                    0,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (90, 21),
                    (99, 28),
                    Unit.SELJUK_GUISARME.value,
                    1,
                    iGameTurn,
                    3,
                    0,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (90, 21),
                    (99, 28),
                    Unit.SELJUK_FOOTMAN.value,
                    1 + iHandicap,
                    iGameTurn,
                    3,
                    0,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (92, 20),
                    (99, 25),
                    Unit.SELJUK_LANCER.value,
                    1,
                    iGameTurn,
                    3,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (92, 20),
                    (99, 25),
                    Unit.TURCOMAN_HORSE_ARCHER.value,
                    1,
                    iGameTurn,
                    3,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (92, 20),
                    (99, 25),
                    Unit.SELJUK_GUISARME.value,
                    1 + iHandicap,
                    iGameTurn,
                    3,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (92, 20),
                    (99, 25),
                    Unit.SELJUK_CROSSBOW.value,
                    1,
                    iGameTurn,
                    3,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (92, 20),
                    (99, 25),
                    Unit.SELJUK_SWORDSMAN.value,
                    1 + iHandicap,
                    iGameTurn,
                    3,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
                )
            elif Civ.ARABIA.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (95, 8),
                    (99, 12),
                    Unit.SELJUK_LANCER.value,
                    1 + iHandicap,
                    iGameTurn,
                    4,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (95, 8),
                    (99, 12),
                    Unit.TURCOMAN_HORSE_ARCHER.value,
                    1,
                    iGameTurn,
                    4,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (95, 8),
                    (99, 12),
                    Unit.SELJUK_GUISARME.value,
                    1,
                    iGameTurn,
                    4,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_SELJUKS", ()),
                )

        # Danishmends
        if DateTurn.i1077AD <= iGameTurn < DateTurn.i1147AD:
            if Civ.BYZANTIUM.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (93, 20),
                    (99, 22),
                    Unit.TURCOMAN_HORSE_ARCHER.value,
                    3 + iHandicap,
                    iGameTurn,
                    5,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_DANISHMENDS", ()),
                )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (93, 20),
                    (99, 22),
                    Unit.TURCOMAN_HORSE_ARCHER.value,
                    2,
                    iGameTurn,
                    5,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_DANISHMENDS", ()),
                )

        # Mongols
        if DateTurn.i1236AD <= iGameTurn < DateTurn.i1288AD:
            # Kiev
            if Civ.KIEV.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (93, 32),
                    (99, 42),
                    Unit.MONGOL_KESHIK.value,
                    5 + iHandicap,
                    iGameTurn,
                    4,
                    0,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (94, 34),
                    (99, 45),
                    Unit.MONGOL_KESHIK.value,
                    4 + iHandicap,
                    iGameTurn,
                    3,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()),
                )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (93, 32),
                    (99, 42),
                    Unit.MONGOL_KESHIK.value,
                    3,
                    iGameTurn,
                    4,
                    0,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (94, 34),
                    (99, 45),
                    Unit.MONGOL_KESHIK.value,
                    2,
                    iGameTurn,
                    3,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()),
                )
            # Hungary
            if Civ.HUNGARY.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (71, 38),
                    (75, 40),
                    Unit.MONGOL_KESHIK.value,
                    4 + iHandicap,
                    iGameTurn,
                    4,
                    2,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (74, 35),
                    (77, 37),
                    Unit.MONGOL_KESHIK.value,
                    2,
                    iGameTurn,
                    4,
                    2,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()),
                )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (71, 38),
                    (75, 40),
                    Unit.MONGOL_KESHIK.value,
                    2,
                    iGameTurn,
                    4,
                    2,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (74, 35),
                    (77, 37),
                    Unit.MONGOL_KESHIK.value,
                    1,
                    iGameTurn,
                    4,
                    2,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()),
                )
            # Poland
            if Civ.POLAND.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (73, 43),
                    (78, 47),
                    Unit.MONGOL_KESHIK.value,
                    5 + iHandicap,
                    iGameTurn,
                    4,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()),
                )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (73, 43),
                    (78, 47),
                    Unit.MONGOL_KESHIK.value,
                    2,
                    iGameTurn,
                    4,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()),
                )
            # Bulgaria
            if Civ.BULGARIA.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (79, 32),
                    (82, 35),
                    Unit.MONGOL_KESHIK.value,
                    3 + iHandicap,
                    iGameTurn,
                    4,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()),
                )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (79, 32),
                    (82, 35),
                    Unit.MONGOL_KESHIK.value,
                    2,
                    iGameTurn,
                    4,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()),
                )
            # Moscow area
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (89, 46),
                (95, 54),
                Unit.MONGOL_KESHIK.value,
                1,
                iGameTurn,
                4,
                0,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (91, 48),
                (97, 53),
                Unit.MONGOL_KESHIK.value,
                2,
                iGameTurn,
                6,
                1,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()),
            )
            # Middle East
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (94, 20),
                (99, 26),
                Unit.MONGOL_KESHIK.value,
                2,
                iGameTurn,
                3,
                2,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()),
            )
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (92, 21),
                (97, 25),
                Unit.MONGOL_KESHIK.value,
                2,
                iGameTurn,
                6,
                1,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_MONGOLS", ()),
            )

        # Timurids, Tamerlane's conquests (aka Mongols, the return!)
        if (
            DateTurn.i1380AD <= iGameTurn <= DateTurn.i1431AD
        ):  # Timur started his first western campaigns in 1380AD
            # Eastern Europe
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (85, 47),
                (99, 57),
                Unit.MONGOL_KESHIK.value,
                2,
                iGameTurn,
                7,
                0,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_TIMURIDS", ()),
            )
            # Anatolia
            if Civ.OTTOMAN.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (87, 17),
                    (96, 24),
                    Unit.MONGOL_KESHIK.value,
                    4 + iHandicap,
                    iGameTurn,
                    4,
                    0,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_TIMURIDS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (94, 18),
                    (99, 26),
                    Unit.MONGOL_KESHIK.value,
                    6 + iHandicap,
                    iGameTurn,
                    5,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_TIMURIDS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (89, 17),
                    (97, 22),
                    Unit.MONGOL_KESHIK.value,
                    3 + iHandicap,
                    iGameTurn,
                    4,
                    2,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_TIMURIDS", ()),
                )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (87, 17),
                    (96, 24),
                    Unit.MONGOL_KESHIK.value,
                    2,
                    iGameTurn,
                    4,
                    0,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_TIMURIDS", ()),
                )
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (94, 18),
                    (99, 26),
                    Unit.MONGOL_KESHIK.value,
                    3,
                    iGameTurn,
                    5,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_TIMURIDS", ()),
                )
            # Arabia
            if Civ.ARABIA.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (96, 9),
                    (99, 15),
                    Unit.MONGOL_KESHIK.value,
                    5 + iHandicap,
                    iGameTurn,
                    4,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_TIMURIDS", ()),
                )
            else:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (96, 9),
                    (99, 15),
                    Unit.MONGOL_KESHIK.value,
                    2,
                    iGameTurn,
                    4,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_TIMURIDS", ()),
                )

        # Nogais
        if DateTurn.i1500AD <= iGameTurn <= DateTurn.i1600AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (93, 38),
                (99, 54),
                Unit.HORSE_ARCHER.value,
                3,
                iGameTurn,
                7,
                1,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_NOGAIS", ()),
            )
            if Civ.MOSCOW.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (93, 38),
                    (99, 54),
                    Unit.HORSE_ARCHER.value,
                    2 + iHandicap,
                    iGameTurn,
                    7,
                    1,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_NOGAIS", ()),
                )

        # Kalmyks
        elif DateTurn.i1600AD <= iGameTurn <= DateTurn.i1715AD:
            self.spawnUnits(
                Civ.BARBARIAN.value,
                (93, 38),
                (99, 54),
                Unit.MONGOL_KESHIK.value,
                3,
                iGameTurn,
                7,
                0,
                utils.forcedInvasion,
                1,
                localText.getText("TXT_KEY_BARBARIAN_NAMES_KALMYKS", ()),
            )
            if Civ.MOSCOW.value == iHuman:
                self.spawnUnits(
                    Civ.BARBARIAN.value,
                    (93, 38),
                    (99, 54),
                    Unit.MONGOL_KESHIK.value,
                    3 + iHandicap,
                    iGameTurn,
                    7,
                    0,
                    utils.forcedInvasion,
                    1,
                    localText.getText("TXT_KEY_BARBARIAN_NAMES_KALMYKS", ()),
                )

        # Independent/barb city spawns and minor nations:
        self.doIndependentCities(iGameTurn)

        if iGameTurn == 1:
            self.setupMinorNation()
        self.doMinorNations(iGameTurn)

    def doIndependentCities(self, iGameTurn):
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
                self.foundCity(iCiv, tCoords, sName, iPop, iUnit, iNumUnits, iReligion, iWorkers)

    def foundCity(
        self, iCiv, tCoords, name, iPopulation, iUnitType, iNumUnits, iReligion, iWorkers
    ):
        if self.checkRegion(tCoords):
            gc.getPlayer(iCiv).found(tCoords[0], tCoords[1])
            city = gc.getMap().plot(tCoords[0], tCoords[1]).getPlotCity()
            city.setName(name, False)
            if iPopulation != 1:
                city.setPopulation(iPopulation)
            if iNumUnits > 0:
                self.makeUnit(iUnitType, iCiv, tCoords, iNumUnits, 0, "")
            if iReligion > -1:
                city.setHasReligion(iReligion, True, True, False)
            if iWorkers > 0:
                self.makeUnit(Unit.WORKER.value, iCiv, tCoords, iWorkers, 0, "")

    def checkRegion(self, tCoords):
        cityPlot = gc.getMap().plot(tCoords[0], tCoords[1])

        # checks if the plot already belongs to someone
        if cityPlot.isOwned():
            if cityPlot.getOwner() != Civ.BARBARIAN.value:
                return False

        # checks the surroundings for cities
        for (x, y) in utils.surroundingPlots(tCoords):
            currentPlot = gc.getMap().plot(x, y)
            if currentPlot.isCity():
                return False
        return True

    def spawnUnits(
        self,
        iCiv,
        tTopLeft,
        tBottomRight,
        iUnitType,
        iNumUnits,
        iTurn,
        iPeriod,
        iRest,
        function,
        iForceAttack,
        szName,
    ):
        if (iTurn % iPeriod) == iRest:
            plotList = utils.squareSearch(tTopLeft, tBottomRight, function, [])
            if plotList:
                tPlot = choice(plotList)
                if tPlot:
                    self.makeUnit(iUnitType, iCiv, tPlot, iNumUnits, iForceAttack, szName)

    def spawnMultiTypeUnits(
        self,
        iCiv,
        tTopLeft,
        tBottomRight,
        lUnitTypes,
        lNumUnits,
        iTurn,
        iPeriod,
        iRest,
        function,
        iForceAttack,
        szName,
    ):
        if (iTurn % iPeriod) == iRest:
            plotList = utils.squareSearch(tTopLeft, tBottomRight, function, [])
            if plotList:
                tPlot = choice(plotList)
                if tPlot:
                    for iUnitType, iNumUnits in zip(lUnitTypes, lNumUnits):
                        self.makeUnit(iUnitType, iCiv, tPlot, iNumUnits, iForceAttack, szName)

    # This is just a clone of spawnUnits but attempting to put a boat under them
    def spawnVikings(
        self,
        iCiv,
        tTopLeft,
        tBottomRight,
        iUnitType,
        iNumUnits,
        iTurn,
        iPeriod,
        iRest,
        function,
        iForceAttack,
        szName,
    ):
        if (iTurn % iPeriod) == iRest:
            plotList = utils.squareSearch(tTopLeft, tBottomRight, function, [])
            if plotList:
                tPlot = choice(plotList)
                if tPlot:
                    pPlayer = gc.getPlayer(iCiv)
                    pUnit = pPlayer.initUnit(
                        Unit.GALLEY.value,
                        tPlot[0],
                        tPlot[1],
                        UnitAITypes.UNITAI_ASSAULT_SEA,
                        DirectionTypes.DIRECTION_SOUTH,
                    )
                    if szName != "":
                        pUnit.setName(szName)
                    self.makeUnit(iUnitType, iCiv, tPlot, iNumUnits, iForceAttack, szName)

    def spawnPirate(
        self,
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
        iForceAttack,
        szName,
    ):
        if (iTurn % iPeriod) == iRest:
            plotList = utils.squareSearch(tTopLeft, tBottomRight, function, [])
            if plotList:
                tPlot = choice(plotList)
                if tPlot:
                    self.makeUnit(iShipType, iCiv, tPlot, iNumShips, 2, szName)
                    self.makeUnit(iFighterType, iCiv, tPlot, iNumFighters, 1, szName)

    def killNeighbours(self, tCoords):
        "Kills all units in the neigbbouring tiles of plot (as well as plot itself) so late starters have some space."
        for (x, y) in utils.surroundingPlots(tCoords):
            killPlot = CyMap().getPlot(x, y)
            for i in range(killPlot.getNumUnits()):
                unit = killPlot.getUnit(
                    0
                )  # killPlot.getUnit(0) instead of killPlot.getUnit(i) because killing units changes the indices
                unit.kill(False, Civ.BARBARIAN.value)

    def onImprovementDestroyed(self, iX, iY):
        # getHandicapType: Viceroy=0, Monarch=1, Emperor=2)
        iHandicap = gc.getGame().getHandicapType()
        iTurn = gc.getGame().getGameTurn()
        if iTurn > DateTurn.i1500AD:
            iBarbUnit = Unit.MUSKETMAN.value
        elif iTurn > DateTurn.i1284AD:
            iBarbUnit = Unit.ARQUEBUSIER.value
        elif iTurn > DateTurn.i840AD:
            iBarbUnit = Unit.HORSE_ARCHER.value
        else:
            iBarbUnit = Unit.SPEARMAN.value
        self.spawnUnits(
            Civ.BARBARIAN.value,
            (iX - 1, iY - 1),
            (iX + 1, iY + 1),
            iBarbUnit,
            1 + iHandicap,
            1,
            1,
            0,
            utils.outerInvasion,
            1,
            "",
        )

    def setupMinorNation(self):
        lNextMinorRevolt = self.getRevolDates()

        for lNation in lMinorNations:
            iNextRevolt = lNation[3][0]
            while iNextRevolt in lNextMinorRevolt:
                iNextRevolt = lNation[3][0] - 3 + rand(6)
            iNationIndex = lMinorNations.index(lNation)
            lNextMinorRevolt[iNationIndex] = iNextRevolt

        self.setRevolDates(lNextMinorRevolt)

    def doMinorNations(self, iGameTurn):
        lNextMinorRevolt = self.getRevolDates()

        if iGameTurn in lNextMinorRevolt:
            # iNation = lNextMinorRevolt.index( iGameTurn )
            lNation = lMinorNations[lNextMinorRevolt.index(iGameTurn)]
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
                    if -1 < iOwner < Civ.POPE.value:  # pope doesn't count here
                        if (
                            iOwner not in lNation[1]
                            and gc.getPlayer(iOwner).getStateReligion() not in lNation[2]
                        ):
                            lPlayersOwning[iOwner] += 1

            for iPlayer in civilizations().main().ids():
                if lPlayersOwning[iPlayer] > 0:
                    if human() == iPlayer:
                        self.doRevoltHuman(iPlayer, iGameTurn, lNation, iRevoltIndex)
                    else:
                        self.doRevoltAI(iPlayer, iGameTurn, lNation, iRevoltIndex)
            # setup next revolt
            iRevoltIndex += 1
            if iRevoltIndex < len(lNation[3]):
                iNextRevolt = lNation[3][iRevoltIndex] - 3 + rand(6)
                while iNextRevolt in lNextMinorRevolt:
                    iNextRevolt = lNation[3][iRevoltIndex] - 3 + rand(6)
                lNextMinorRevolt[lNextMinorRevolt.index(iGameTurn)] = iNextRevolt
                self.setRevolDates(lNextMinorRevolt)

    def doRevoltAI(self, iPlayer, iGameTurn, lNation, iRevoltIndex):
        cityList = self.getProvincePlayerCityList(lNation[0], iPlayer)

        iNumGarrison = 0
        for iI in range(len(cityList)):
            iNumGarrison += self.getGarrasonSize(cityList[iI])

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
                self.makeRebels(
                    pCity, lNation[5][iRevoltIndex], lNation[6][iRevoltIndex], lNation[7][1]
                )
        else:
            # revolt succeeded
            lIndependents = [
                Civ.INDEPENDENT.value,
                Civ.INDEPENDENT_2.value,
                Civ.INDEPENDENT_3.value,
                Civ.INDEPENDENT_4.value,
            ]
            iNewCiv = choice(lIndependents)
            for iI in range(len(cityList)):
                pCity = cityList[iI]
                tCity = (pCity.getX(), pCity.getY())
                utils.cultureManager(tCity, 50, iNewCiv, iPlayer, False, True, True)
                utils.flipUnitsInCitySecession(tCity, iNewCiv, iPlayer)
                self.setTempFlippingCity(tCity)
                utils.flipCity(
                    tCity, 0, 0, iNewCiv, [iPlayer]
                )  # by trade because by conquest may raze the city
                utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)

    def showPopup(self, popupID, title, message, labels):
        popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
        popup.setHeaderString(title)
        popup.setBodyString(message)
        for i in labels:
            popup.addButton(i)
        popup.launch(False)

    def eventApply7627(self, popupReturn):
        iDecision = popupReturn.getButtonClicked()
        iNationIndex, iRevoltIndex = self.getNationRevoltIndex()
        lNation = lMinorNations[iNationIndex]
        iPlayer = human()

        cityList = self.getProvincePlayerCityList(lNation[0], iPlayer)

        iNumGarrison = 0
        iBribeGold = 0
        for iI in range(len(cityList)):
            iNumGarrison += self.getGarrasonSize(cityList[iI])
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
            if iGovernment == Civic.DESPOTISM.value:
                iBribeOdds = 15
            elif iGovernment == Civic.FEUDAL_MONARCHY.value:
                iBribeOdds = 25
            elif iGovernment == Civic.DIVINE_MONARCHY.value:
                iBribeOdds = 30
            elif iGovernment == Civic.LIMITE_DMONARCHY.value:
                iBribeOdds = 25
            elif iGovernment == Civic.MERCHANT_REPUBLIC.value:
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
                CyInterface().addMessage(
                    iPlayer,
                    False,
                    MessageData.DURATION,
                    CyTranslator().getText(
                        "TXT_KEY_MINOR_NATION_REVOLT_SUPRESSED", (pCity.getName(),)
                    ),
                    "",
                    0,
                    "",
                    ColorTypes(MessageData.BLUE),
                    -1,
                    -1,
                    True,
                    True,
                )
                # cracking the rebels results in unhappiness in the general population:
                if iDecision in [1, 3]:
                    pCity.changeHurryAngerTimer(10)
                    pCity.changeOccupationTimer(1)
                # bribing their lords away from their cause angers the rebel militia further:
                if iDecision in [2, 3]:
                    self.makeRebels(
                        pCity,
                        lNation[5][iRevoltIndex],
                        1 + lNation[6][iRevoltIndex],
                        lNation[7][1],
                    )
                else:
                    self.makeRebels(
                        pCity, lNation[5][iRevoltIndex], lNation[6][iRevoltIndex], lNation[7][1]
                    )
        else:
            # revolt succeeded
            lIndependents = [
                Civ.INDEPENDENT.value,
                Civ.INDEPENDENT_2.value,
                Civ.INDEPENDENT_3.value,
                Civ.INDEPENDENT_4.value,
            ]
            iNewCiv = choice(lIndependents)
            for iI in range(len(cityList)):
                pCity = cityList[iI]
                tCity = (pCity.getX(), pCity.getY())
                sNationName = localText.getText(lNation[7][1], ())
                CyInterface().addMessage(
                    iPlayer,
                    False,
                    MessageData.DURATION,
                    CyTranslator().getText(
                        "TXT_KEY_MINOR_NATION_REVOLT_SUCCEEDED",
                        (
                            sNationName,
                            pCity.getName(),
                        ),
                    ),
                    "",
                    0,
                    "",
                    ColorTypes(MessageData.ORANGE),
                    -1,
                    -1,
                    True,
                    True,
                )
                utils.cultureManager(tCity, 50, iNewCiv, iPlayer, False, True, True)
                utils.flipUnitsInCitySecession(tCity, iNewCiv, iPlayer)
                self.setTempFlippingCity(tCity)
                utils.flipCity(
                    tCity, 0, 0, iNewCiv, [iPlayer]
                )  # by trade because by conquest may raze the city
                utils.flipUnitsInCityAfter(self.getTempFlippingCity(), iNewCiv)

    # Absinthe: revolution choice effects:
    # base chance: stability bonus adjusted with the revolt strength + base chance + passive military presence - revolt strength
    # suppress with force: + base chance + military strength in the city. revolt +1 turn, unhappy +1 for 10 turns
    # bribe the lords: + financial chance: costs 10 gold per population, suppression depends on the government Divine Monarchy (30%), Feudal or Limited (25%), Merchant (20%), Decentral (15%)
    def doRevoltHuman(self, iPlayer, iGameTurn, lNation, iRevoltIndex):
        self.setNationRevoltIndex(lMinorNations.index(lNation), iRevoltIndex)

        cityList = self.getProvincePlayerCityList(lNation[0], iPlayer)

        iNumGarrison = 0
        iBribeGold = 0
        for iI in range(len(cityList)):
            iNumGarrison += self.getGarrasonSize(cityList[iI])
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
        if iGovernment == Civic.DESPOTISM.value:
            iBribeOdds = 15
        elif iGovernment == Civic.FEUDAL_MONARCHY.value:
            iBribeOdds = 25
        elif iGovernment == Civic.DIVINE_MONARCHY.value:
            iBribeOdds = 30
        elif iGovernment == Civic.LIMITE_DMONARCHY.value:
            iBribeOdds = 25
        elif iGovernment == Civic.MERCHANT_REPUBLIC.value:
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

        szRebellName = localText.getText(lNation[7][0], ())
        self.showPopup(
            7627,
            localText.getText("TXT_KEY_MINOR_REBELLION_TITLE", (szRebellName,)),
            localText.getText("TXT_KEY_MINOR_REBELLION_DESC", (szRebellName,)),
            (
                localText.getText("TXT_KEY_MINOR_REBELLION_DO_NOTHING", (iRawOdds,)),
                localText.getText("TXT_KEY_MINOR_REBELLION_CRACK", (iCrackOdds,)),
                localText.getText(
                    "TXT_KEY_MINOR_REBELLION_BRIBE",
                    (
                        iGold,
                        iBribeGold,
                        iBribeOdds,
                    ),
                ),
                localText.getText("TXT_KEY_MINOR_REBELLION_ALL", (iAllOdds,)),
            ),
        )

    def getGarrasonSize(self, pCity):
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

    def makeRebels(self, pCity, iUnit, iCount, szName):
        lAvailableFreeTiles = []
        lAvailableTiles = []
        iTX = pCity.getX()
        iTY = pCity.getY()
        for (x, y) in utils.surroundingPlots((iTX, iTY)):
            pPlot = gc.getMap().plot(x, y)
            if pPlot.isHills() or pPlot.isFlatlands():
                if not pPlot.isCity():
                    if pPlot.getNumUnits() == 0:
                        lAvailableFreeTiles.append((x, y))
                    else:
                        lAvailableTiles.append((x, y))

        if lAvailableFreeTiles:
            tPlot = choice(lAvailableFreeTiles)
        elif lAvailableTiles:
            # if all tiles are taken, select one tile at random and kill all units there
            tPlot = choice(lAvailableTiles)
            pPlot = gc.getMap().plot(tPlot[0], tPlot[1])
            iN = pPlot.getNumUnits()
            for i in range(iN):
                pPlot.getUnit(0).kill(False, Civ.BARBARIAN.value)
        else:
            return

        pBarb = gc.getPlayer(Civ.BARBARIAN.value)
        for iI in range(iCount):
            pUnit = pBarb.initUnit(
                iUnit,
                tPlot[0],
                tPlot[1],
                UnitAITypes.UNITAI_ATTACK,
                DirectionTypes.DIRECTION_SOUTH,
            )
            pUnit.setName(localText.getText(szName, ()))

    def getProvincePlayerCityList(self, iProvince, iPlayer):
        return [city for city in utils.getCityList(iPlayer) if city.getProvince() == iProvince]
