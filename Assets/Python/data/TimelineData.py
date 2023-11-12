# -*- coding: utf-8 -*-

from CoreStructures import CivDataMapper, CompanyDataMapper
from CoreTypes import Civ, Company, Technology

# TODO switch to years with convert from trun
# TODO fix company birth dates
# TODO change  behavior in order to replace default values like 999 with None

# Timeline of the mod, all important years to be references by year as opposed to hard-to-follow turn numbers
# Important event Spawn UHV
class DateTurn:
    i500AD = 0
    i508AD = 2
    i520AD = 5
    i540AD = 10  # Gothic wars: Ravenna reconquered
    i552AD = 13
    i568AD = 17
    i600AD = 25  # Stirrup in the beginning of the 7th century
    i632AD = 33  # Spawn of Arabia / Byzantium UHV 1
    i635AD = 34
    i640AD = 35
    i660AD = 40
    i670AD = 43
    i680AD = 45  # Spawn of Bulgaria
    i700AD = 50
    i711AD = 53  # Spawn of Cordoba
    i712AD = 53
    i720AD = 55
    i752AD = 63
    i760AD = 65
    i768AD = 67
    i770AD = 68
    i778AD = 69
    i780AD = 70
    i800AD = 75
    i810AD = 78  # Spawn of Venice
    i840AD = 85  # France UHV 1
    i843AD = 86  # Treaty of Verdun / Spawn of Burgundy
    i844AD = 86
    i850AD = 88  # Greatest extent of the Abbasid Caliphate / Arabia UHV 1
    i852AD = 88
    i856AD = 89  # Spawn of Germany
    i860AD = 90
    i864AD = 91  # Rus' capital moved to Novgorod / Spawn of Novgorod
    i867AD = 92
    i872AD = 93  # Spawn of Norway
    i880AD = 95
    i882AD = 95  # Spawn of Kiev
    i892AD = 98
    i895AD = 99  # Honfoglalas / Spawn of Hungary
    i900AD = 100
    i910AD = 103  # Kingdom of Leon / Spawn of Spain
    i911AD = 104  # Establishment of the Duchy of Normandy
    i917AD = 106  # Bulgaria UHV 1
    i920AD = 107  # Kievan Rus - Pecheneg Wars
    i925AD = 108
    i936AD = 112  # Spawn of Denmark
    i940AD = 113
    i955AD = 118  # Basil defeats the Arabs
    i960AD = 120  # Spawn of Scotland
    i961AD = 120  # Cordoba UHV 1
    i962AD = 121  # HRE founded
    i966AD = 122  # Spawn of Poland
    i970AD = 123
    i972AD = 124
    i983AD = 128
    i987AD = 129
    i988AD = 129
    i1000AD = 133  # Start of the Defensive Crusades
    i1003AD = 134
    i1004AD = 135  # Venice UHV 1
    i1009AD = 136
    i1010AD = 137
    i1016AD = 139  # Muslims are defeated in Sardinia / Spawn of Genoa
    i1020AD = 140
    i1025AD = 142  # Death of Basil II
    i1032AD = 144
    i1040AD = 147  # Spawn of Morocco
    i1050AD = 150  # Denmark UHV 1
    i1053AD = 151
    i1057AD = 152
    i1060AD = 153  # First Crusade gets called
    i1061AD = 154
    i1064AD = 155  # Seljuk invasions begin
    i1066AD = 155  # Battle of Hastings / Spawn of England / Norway UHV 1
    i1067AD = 156
    i1077AD = 159
    i1080AD = 160
    i1085AD = 162
    i1089AD = 163
    i1094AD = 165
    i1096AD = 165  # First Crusade 1096-1099
    i1097AD = 166
    i1099AD = 166  # Conquest of Jerusalem
    i1101AD = 167
    i1107AD = 169  # Norwegian Crusade (1107-1110)
    i1110AD = 170
    i1120AD = 173
    i1124AD = 175
    i1136AD = 179  # Traditional beginning of the Novgorod Republic
    i1139AD = 180  # Spawn of Portugal
    i1144AD = 181  # Alchemy introduced in Europe
    i1147AD = 182  # Second Crusade 1147-1149
    i1150AD = 183  # First Swedish "Crusade"
    i1160AD = 187
    i1164AD = 188  # Spawn of Aragon
    i1167AD = 189  # Barbarossa wins against Rome / Germany UHV 1
    i1171AD = 190
    i1180AD = 193
    i1185AD = 195  # Rise of the 2nd Bulgarian Empire
    i1187AD = 196  # Third Crusade 1187-1192
    i1194AD = 198  # End of Norman rule in Sicily / Norway UHV 2
    i1198AD = 199  # German Crusade (1195–1198)
    i1200AD = 200
    i1202AD = 201  # Fourth Crusade 1202-1204
    i1204AD = 201  # Venice UHV 2
    i1210AD = 203  # Spawn of Sweden
    i1212AD = 204
    i1217AD = 206  # Fifth Crusade 1217-1221
    i1219AD = 206
    i1224AD = 208  # Spawn of Prussia
    i1227AD = 209
    i1229AD = 210  # Sixth Crusade 1228-1229
    i1230AD = 210
    i1236AD = 212  # Mongol invasions / Spawn of Lithuania
    i1240AD = 213  # Second Swedish "Crusade"
    i1242AD = 214  # Battle on the Ice
    i1248AD = 216  # Seventh Crusade 1248-1254, Fall of Cordoban Seville / Morocco UHV 1
    i1250AD = 217  # Kiev UHV 1
    i1259AD = 220  # Bulgaria UHV 2
    i1263AD = 221
    i1269AD = 223
    i1271AD = 224  # Eighth and Ninth Crusade 1270-1272
    i1281AD = 227
    i1282AD = 227  # Rise of the Habsburgs / Spawn of Austria / Byzantium UHV 2, Aragon UHV 1
    i1284AD = 228  # Aragonese Crusade (1284-1285) / Novgorod UHV 1
    i1288AD = 230  # End of the fist wave of Mongols / Kiev UHV 2
    i1291AD = 230  # Arabia UHV 2, France UHV 2
    i1293AD = 231  # Third Swedish "Crusade"
    i1296AD = 232  # Scotland UHV 1
    i1297AD = 232
    i1299AD = 233
    i1300AD = 233  # Kiev UHV 3
    i1309AD = 236  # Cordoba UHV 2
    i1320AD = 240  # Norway UHV 3
    i1323AD = 241  # Sweden UHV 1
    i1328AD = 243
    i1336AD = 245  # Burgundy UHV 1
    i1346AD = 248
    i1348AD = 249
    i1350AD = 250
    i1354AD = 251  # Earthquake of Gallipoli
    i1356AD = 252  # Spawn of the Ottomans
    i1359AD = 253
    i1362AD = 254  # Conquest of Adrianopolis
    i1371AD = 257
    i1376AD = 259  # Burgundy UHV 2
    i1377AD = 259
    i1380AD = 260  # Spawn of Moscow
    i1386AD = 262  # Lithuania UHV 1
    i1393AD = 264
    i1396AD = 265  # Battle of Nicopolis / Bulgaria UHV 3
    i1397AD = 266  # Kalmar Union / Novgorod UHV 2
    i1400AD = 267  # Genoa UHV 1
    i1401AD = 267
    i1410AD = 270  # Battle of Grunwald / Prussia UHV 1
    i1419AD = 273
    i1430AD = 277  # Death of Vytatutas (Lithuania greatest extent) / Lithuania UHV 2
    i1431AD = 277
    i1441AD = 280
    i1444AD = 281  # Battle of Varna, Hunyadi's Balkan Campaign / Aragon UHV 2
    i1449AD = 283
    i1452AD = 284  # End of the Hundred Years war / English UHV 1
    i1453AD = 284  # Conquest of Constantinople / Byzantium UHV 3
    i1461AD = 287
    i1465AD = 288  # Morocco UHV 2
    i1470AD = 290
    i1473AD = 291  # Burgundy UHV 3
    i1474AD = 291  # Aragon UHV 3
    i1478AD = 293  # Annexation of Novgorod / Novgorod UHV 3
    i1482AD = 294  # Moscow UHV 1
    i1490AD = 297  # Hungary UHV 1
    i1491AD = 297
    i1492AD = 297  # Cordoba UHV 3, Spain UHV 1
    i1494AD = 298
    i1500AD = 300  # Poland UHV 1 (start)
    i1514AD = 307  # Copernicus
    i1517AD = 308  # Printing Press / Ottoman UHV 1
    i1520AD = 310  # Poland UHV 1 (end)
    i1523AD = 311  # Denmark UHV 2
    i1525AD = 312
    i1526AD = 313  # Battle of Mohács, Ottoman invasion of Hungary
    i1530AD = 315
    i1540AD = 320
    i1541AD = 321  # Buda is lost to the Ottomans / Hungary UHV 2
    i1542AD = 321
    i1544AD = 322
    i1560AD = 330  # Scotland UHV 2
    i1566AD = 333  # Loss of Chios and the Genoese trade routes / Genoa UHV 3
    i1569AD = 334  # Union of Lublin / Poland UHV 2
    i1570AD = 335
    i1571AD = 336
    i1578AD = 339  # Morocco UHV 3
    i1580AD = 340
    i1581AD = 340  # Spawn of the Dutch
    i1588AD = 344  # Spain UHV 2
    i1600AD = 350
    i1616AD = 358  # Ottoman UHV 2
    i1617AD = 358  # Austria UHV 1
    i1618AD = 359  # Brandenburg-Prussia, Start of Thirty Years War
    i1620AD = 360
    i1623AD = 361  # Galileo
    i1625AD = 362
    i1631AD = 365
    i1640AD = 370  # Portugal UHV 2
    i1648AD = 374  # End of Thirty Years War / Germany UHV 3, Spain UHV 3
    i1650AD = 375  # Prussia UHV 2 (start)
    i1660AD = 380  # Sweden UHV 2
    i1670AD = 385
    i1680AD = 390
    i1683AD = 391  # Ottoman UHV 3
    i1687AD = 393
    i1690AD = 395  # Steam Engine
    i1699AD = 399
    i1700AD = 400  # Austria UHV 2, Scotland UHV 3
    i1707AD = 407  # Act of Union
    i1715AD = 415
    i1730AD = 430
    i1750AD = 450  # Dutch UHV 1, Sweden UHV 3
    i1763AD = 463  # Prussia UHV 2 (end)
    i1780AD = 480  # Austria UHV 3
    i1795AD = 495  # Partition of Poland / Lithuania UHV 3
    i1800AD = 500  # Industrial Era


CIV_BIRTHDATE = CivDataMapper(
    {
        Civ.BYZANTIUM: DateTurn.i500AD,
        Civ.FRANCE: DateTurn.i500AD,
        Civ.ARABIA: DateTurn.i632AD,
        Civ.BULGARIA: DateTurn.i680AD,
        Civ.CORDOBA: DateTurn.i711AD,
        Civ.VENECIA: DateTurn.i810AD,
        Civ.BURGUNDY: DateTurn.i843AD,
        Civ.GERMANY: DateTurn.i856AD,
        Civ.NOVGOROD: DateTurn.i864AD,
        Civ.NORWAY: DateTurn.i872AD,
        Civ.KIEV: DateTurn.i882AD,
        Civ.HUNGARY: DateTurn.i895AD,
        Civ.CASTILE: DateTurn.i910AD,
        Civ.DENMARK: DateTurn.i936AD,
        Civ.SCOTLAND: DateTurn.i960AD,
        Civ.POLAND: DateTurn.i966AD,
        Civ.GENOA: DateTurn.i1016AD,
        Civ.MOROCCO: DateTurn.i1040AD,
        Civ.ENGLAND: DateTurn.i1066AD,
        Civ.PORTUGAL: DateTurn.i1139AD,
        Civ.ARAGON: DateTurn.i1164AD,
        Civ.SWEDEN: DateTurn.i1210AD,
        Civ.PRUSSIA: DateTurn.i1224AD,
        Civ.LITHUANIA: DateTurn.i1236AD,
        Civ.AUSTRIA: DateTurn.i1282AD,
        Civ.OTTOMAN: DateTurn.i1356AD,
        Civ.MOSCOW: DateTurn.i1380AD,
        Civ.DUTCH: DateTurn.i1581AD,
    }
).fill_missing_members(DateTurn.i500AD)

# Gives a stability penalty to AI civs past this date
CIV_COLLAPSE_DATE = CivDataMapper(
    {
        Civ.BYZANTIUM: DateTurn.i1453AD,
        Civ.ARABIA: DateTurn.i1517AD,
        Civ.BULGARIA: DateTurn.i1396AD,
        Civ.CORDOBA: DateTurn.i1492AD,
        Civ.BURGUNDY: DateTurn.i1473AD,
        Civ.GERMANY: DateTurn.i1648AD,
        Civ.NOVGOROD: DateTurn.i1478AD,
        Civ.NORWAY: DateTurn.i1523AD,
        Civ.KIEV: DateTurn.i1300AD,
        Civ.HUNGARY: DateTurn.i1542AD,
        Civ.SCOTLAND: DateTurn.i1650AD,
        Civ.POLAND: DateTurn.i1780AD,
        Civ.GENOA: DateTurn.i1500AD,
        Civ.ARAGON: DateTurn.i1474AD,
        Civ.LITHUANIA: DateTurn.i1569AD,
    }
).fill_missing_members(999)

CIV_RESPAWNING_DATE = CivDataMapper(
    {
        Civ.FRANCE: DateTurn.i1600AD,
        Civ.ARABIA: DateTurn.i1107AD,
        Civ.BULGARIA: DateTurn.i1185AD,
        Civ.CORDOBA: DateTurn.i1229AD,
        Civ.BURGUNDY: DateTurn.i1336AD,
        Civ.KIEV: DateTurn.i1648AD,
        Civ.HUNGARY: DateTurn.i1687AD,
        Civ.CASTILE: DateTurn.i1470AD,
        Civ.DENMARK: DateTurn.i1359AD,
        Civ.SCOTLAND: DateTurn.i1296AD,
        Civ.POLAND: DateTurn.i1410AD,
        Civ.MOROCCO: DateTurn.i1631AD,
        Civ.ENGLAND: DateTurn.i1660AD,
        Civ.PORTUGAL: DateTurn.i1400AD,
        Civ.ARAGON: DateTurn.i1500AD,
        Civ.SWEDEN: DateTurn.i1523AD,
        Civ.PRUSSIA: DateTurn.i1618AD,
        Civ.AUSTRIA: DateTurn.i1526AD,
        Civ.OTTOMAN: DateTurn.i1482AD,
    }
).fill_missing_members(999)

# TODO fix dates
COMPANY_BIRTHDATE = CompanyDataMapper(
    {
        Company.HOSPITALLERS: DateTurn.i1096AD,
        Company.TEMPLARS: DateTurn.i1096AD,
        Company.TEUTONS: DateTurn.i1096AD,
        Company.HANSA: 186,  # 1157
        Company.MEDICI: DateTurn.i1397AD,
        Company.AUGSBURG: 295,  # 1487
        Company.ST_GEORGE: 269,  # 1407
        Company.DRAGON: 269,  # 1408
        Company.CALATRAVA: DateTurn.i1164AD,
    }
)

COMPANY_DEATHDATE = CompanyDataMapper(
    {
        Company.TEMPLARS: DateTurn.i1309AD,
        Company.HANSA: DateTurn.i1670AD,
        Company.MEDICI: DateTurn.i1500AD,
        Company.ST_GEORGE: DateTurn.i1800AD,
        Company.CALATRAVA: DateTurn.i1800AD,
    }
).fill_missing_members(999)

# Used by GameBalance
TIMELINE_TECH_MODIFIER = [
    (Technology.CALENDAR, 0),
    (Technology.ARCHITECTURE, 30),
    (Technology.BRONZE_CASTING, 15),
    (Technology.THEOLOGY, 10),
    (Technology.MANORIALISM, 5),
    (Technology.STIRRUP, DateTurn.i600AD),
    (Technology.ENGINEERING, 55),
    (Technology.CHAIN_MAIL, 43),
    (Technology.ART, 38),
    (Technology.MONASTICISM, 50),
    (Technology.VASSALAGE, 60),
    (Technology.ASTROLABE, 76),
    (Technology.MACHINERY, 76),
    (Technology.VAULTED_ARCHES, 90),
    (Technology.MUSIC, 80),
    (Technology.HERBAL_MEDICINE, 95),
    (Technology.FEUDALISM, DateTurn.i778AD),
    (Technology.FARRIERS, 100),
    (Technology.MAPMAKING, 160),
    (Technology.BLAST_FURNACE, 120),
    (Technology.SIEGE_ENGINES, DateTurn.i1097AD),
    (Technology.GOTHIC_ARCHITECTURE, 130),
    (Technology.LITERATURE, 145),
    (Technology.CODE_OF_LAWS, 120),
    (Technology.ARISTOCRACY, 135),
    (Technology.LATEEN_SAILS, 125),
    (Technology.PLATE_ARMOR, 185),
    (Technology.MONUMENT_BUILDING, 180),
    (Technology.CLASSICAL_KNOWLEDGE, 175),
    (Technology.ALCHEMY, DateTurn.i1144AD),
    (Technology.CIVIL_SERVICE, 190),
    (Technology.CLOCKMAKING, 200),
    (Technology.PHILOSOPHY, 215),
    (Technology.EDUCATION, 220),
    (Technology.GUILDS, 200),
    (Technology.CHIVALRY, 195),
    (Technology.OPTICS, 228),
    (Technology.REPLACEABLE_PARTS, 250),
    (Technology.PATRONAGE, 230),
    (Technology.GUNPOWDER, DateTurn.i1300AD),
    (Technology.BANKING, 240),
    (Technology.MILITARY_TRADITION, 260),
    (Technology.SHIP_BUILDING, 275),
    (Technology.DRAMA, 270),
    (Technology.DIVINE_RIGHT, 266),
    (Technology.CHEMISTRY, 280),
    (Technology.PAPER, 290),
    (Technology.PROFESSIONAL_ARMY, 295),
    (Technology.PRINTING_PRESS, DateTurn.i1517AD),
    (Technology.PUBLIC_WORKS, 310),
    (Technology.MATCH_LOCK, DateTurn.i1500AD),
    (Technology.ARABIC_KNOWLEDGE, DateTurn.i1491AD),
    (Technology.ASTRONOMY, DateTurn.i1514AD),
    (Technology.STEAM_ENGINES, DateTurn.i1690AD),
    (Technology.CONSTITUTION, 375),
    (Technology.POLYGONAL_FORT, 370),
    (Technology.ARABIC_MEDICINE, 342),
    (Technology.RENAISSANCE_ART, DateTurn.i1540AD),
    (Technology.NATIONALISM, 380),
    (Technology.LIBERALISM, 400),
    (Technology.SCIENTIFIC_METHOD, DateTurn.i1623AD),
    (Technology.MILITARY_TACTICS, 410),
    (Technology.NAVAL_ARCHITECTURE, 385),
    (Technology.CIVIL_ENGINEERING, 395),
    (Technology.RIGHT_OF_MAN, 460),
    (Technology.ECONOMICS, 435),
    (Technology.PHYSICS, DateTurn.i1687AD),
    (Technology.BIOLOGY, 440),
    (Technology.COMBINED_ARMS, 430),
    (Technology.TRADING_COMPANIES, DateTurn.i1600AD),
    (Technology.MACHINE_TOOLS, 450),
    (Technology.FREE_MARKET, 450),
    (Technology.EXPLOSIVES, 460),
    (Technology.MEDICINE, 458),
    (Technology.INDUSTRIAL_TECH, DateTurn.i1800AD),
]
