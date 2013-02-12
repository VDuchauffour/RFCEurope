# Rhye's and Fall of Civilization - Constants

# globals

#from CvPythonExtensions import *
#gc = CyGlobalContext()

import XMLConsts as xml

l0Array =       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 3Miro for stability, counts the cities for each player
l0ArrayActive = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
l0ArrayTotal =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # this is just a dummy array

lm1Array =      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
# Size of the above are final size

# 3Miro: map size entered here
iMapMaxX = 100
iMapMaxY = 73

#### Chronological order
# Byzantium   i500AD
# France      i500AD
# Arabia      i632AD
# Bulgaria    i680AD
# Cordoba     i711AD
# Norse       i780AD
# Venice      i810AD
# Burgundy    i843AD
# Germany     i858AD
# Kiev        i880AD
# Hungary     i895AD
# Spain       i909AD
# Poland      i966AD
# Genoa       i1016AD
# England     i1066AD
# Portugal    i1139AD
# Lithuania   i1236AD
# Austria     i1282AD
# Turkey      i1359AD
# Moscow      i1380AD
# Sweden      i1523AD
# Dutch       i1581AD
# Pope - keep him last

# initialise player variables to player IDs from WBS (this is the only part of the XML that will stay here)
iByzantium = 0
iFrankia = 1
iArabia = 2
iBulgaria = 3
iCordoba = 4
iNorse = 5
iVenecia = 6
iBurgundy = 7
iGermany = 8
iKiev = 9
iHungary = 10
iSpain = 11
iPoland = 12
iGenoa = 13
iEngland = 14
iPortugal = 15
iLithuania = 16
iAustria = 17
iTurkey = 18
iMoscow = 19
iSweden = 20
iDutch = 21
iPope = 22
iNumPlayers = 23
iNumMajorPlayers = 23
iNumActivePlayers = 23
iIndependent = 23
iIndependent2 = 24
iIndependent3 = 25
iIndependent4 = 26
iNumTotalPlayers = 27
iBarbarian = 27
iNumTotalPlayersB = 28

iIndepStart = iIndependent # creates a block of independent civs
iIndepEnd = iIndependent4

#for Congresses and Victory
lCivGroups = [[iByzantium,iBulgaria,iKiev,iLithuania,iMoscow],		#Eastern
		[iBurgundy,iHungary,iGermany,iPoland,iAustria],		#Central
		[iFrankia,iSpain,iEngland,iPortugal,iDutch],	#Atlantic
		[iArabia,iCordoba,iTurkey],			#Islamic
		[iGenoa,iVenecia,iPope],		#Italian
		[iNorse,iSweden]] 			#Scandinavian

lCivStabilityGroups = [[iByzantium,iBulgaria,iKiev,iLithuania,iMoscow],	#Eastern
			[iBurgundy,iHungary,iGermany,iPoland,iAustria],		#Central
			[iFrankia,iSpain,iEngland,iPortugal,iDutch],	#Atlantic
			[iArabia,iCordoba,iTurkey],		#Islamic
			[iGenoa,iVenecia,iPope],	#Italian
			[iNorse,iSweden]]		#Norse

lCivBioOldWorld = [iByzantium, iBulgaria, iBurgundy, iArabia, iFrankia, iSpain, iCordoba, iNorse, iVenecia, iKiev, iHungary, \
			iGermany, iPoland, iMoscow, iGenoa, iEngland, iPortugal, iLithuania, iAustria, iTurkey, iSweden, iDutch, iPope, \
			iIndependent, iIndependent2, iBarbarian]

lCivBioNewWorld = []

#for messages
iDuration = 14
iWhite = 0
iRed = 7
iGreen = 8
iBlue = 9
iLightBlue = 10
iYellow = 11
iDarkPink = 12
iLightRed = 20
iPurple = 25
iCyan = 44
iBrown = 55
iOrange = 88
iTan = 90
iLime = 100

#neighbours
lNeighbours = [
[iBulgaria,iArabia,iTurkey],	#Byzantium
[iBurgundy,iEngland],	#Frankia
[iByzantium,iTurkey],			#Arabia
[iByzantium,iHungary,iKiev],	#Bulgaria
[iSpain,iPortugal],		#Cordoba
[iSweden,iGermany],			#Norse
[iGenoa,iGermany,iAustria,iHungary,iPope],		#Venice
[iFrankia,iDutch,iGermany],		#Burgundy
[iBurgundy,iDutch,iAustria,iVenecia,iGenoa,iPoland,iHungary,iNorse],	#Germany
[iBulgaria,iMoscow,iPoland],		#Kiev
[iBulgaria,iVenecia,iPoland,iGermany,iAustria],			#Hungary
[iCordoba,iPortugal],	#Spain
[iGermany,iAustria,iHungary,iKiev,iMoscow,iLithuania],			#Poland
[iGermany,iVenecia,iBurgundy,iPope],	#Genoa
[iFrankia,iDutch],			#England
[iSpain,iCordoba],			#Portugal
[iKiev,iPoland,iMoscow],		#Lithuania
[iGermany,iHungary,iPoland,iVenecia],	#Austria
[iByzantium,iArabia],			#Turkey
[iKiev,iPoland,iLithuania],		#Moscow
[iNorse,iLithuania],				#Sweden
[iGermany,iEngland,iBurgundy],		#Dutch
[iVenecia, iGenoa]			#Pope
]

#for stability hit on spawn
lOlderNeighbours = [
[], #Byzantium
[], #Frankia
[iByzantium], #Arabia
[iByzantium], #Bulgaria
[], #Cordoba
[], #Norse
[iCordoba], #Venice
[], #Burgundy
[], #Germany
[iBulgaria], #Kiev
[iBulgaria], #Hungary
[iCordoba], #Spain
[iGermany,iKiev], #Poland
[iVenecia,iGermany,iCordoba], #Genoa
[iFrankia], #England
[iSpain,iCordoba], #Portugal
[iPoland], #Lithuania
[iGermany,iHungary,iVenecia,iGenoa], #Austria
[iByzantium,iBulgaria,iCordoba,iArabia], #Turkey
[iKiev,iPoland,iLithuania], #Moscow
[iNorse,iPoland,iMoscow,iLithuania], #Sweden
[iGermany,iFrankia], #Dutch
[] #Pope
]

# civ birth dates
tBirth = (
xml.i500AD, #500AD Byzantium
xml.i500AD, #500AD Frankia
xml.i632AD, #632AD Arabia
xml.i680AD, #680AD Bulgaria
xml.i711AD, #711AD Cordoba
xml.i780AD, #780AD Norse
xml.i810AD, #810AD Venice
xml.i843AD, #843AD Burgundy
xml.i858AD, #858AD Germany
xml.i880AD, #880AD Kiev # There is an Autorun Bug, usually Kiev and Hungary play one extra turn (but not always)
xml.i895AD, #895AD Hungary # There is an Autorun Bug, usually Kiev and Hungary play one extra turn (but not always)
xml.i910AD, #909AD Spain
xml.i966AD, #966AD Poland
xml.i1016AD,#1016AD Genoa
xml.i1066AD,#1066AD England
xml.i1139AD,#1139AD Portugal
xml.i1236AD,#1236AD Lithuania
xml.i1282AD,#1282AD Austria
xml.i1359AD,#1359AD Turkey - turn 233 is normal time (Conquest of Adrianopolis)
xml.i1380AD,#1380AD Moscow
xml.i1523AD,#1523AD Sweden
xml.i1581AD,#1581AD Dutch - turn 340 is normal time
0, #Pope
0,
0,
0,
0,
0
) # 3Miro: tBirth should finish with zeros for all minor civs (the 4 independents and the barbs)

# "Collapse dates", gives a stability penalty to AI civs past this date. The idea is to speed up late game a bit - from RFCE++
# Currently the penalty is small, mostly to weaken the civs if they are powerful
tCollapse = (
xml.i1453AD, #Byzantium - Ottoman conquest of Constantinople
999, #Frankia
xml.i1517AD, #Arabia - to make room for the Ottomans
xml.i1393AD, #Bulgaria - Bulgaria UHV 3
xml.i1492AD, #Cordoba - Cordoba UHV 3
999, #Norse
999, #Venice
xml.i1473AD, #Burgundy - Burgundy UHV 3
999, #Germany ##in RFCE++: xml.i1648AD, #Germany - to make room for Prussia
xml.i1300AD, #Kiev - Kiev UHV 1
xml.i1542AD, #Hungary - 1541, Ottoman conquest of Buda
999, #Spain
xml.i1780AD, #Poland
xml.i1500AD, #Genoa
999, #England
999, #Portugal
xml.i1569AD, #Lithuania - Lithuania UHV 3
999, #Austria
999, #Turkey
999, #Moscow
999, #Sweden
999, #Dutch
999  #Pope
)

tYear = ( #For the Dawn of Man starting screen
("500", "TXT_KEY_AD"),
("500", "TXT_KEY_AD"),
("635", "TXT_KEY_AD"),
("680", "TXT_KEY_AD"),
("711", "TXT_KEY_AD"),
("780", "TXT_KEY_AD"),
("810", "TXT_KEY_AD"),
("843", "TXT_KEY_AD"),
("858", "TXT_KEY_AD"),
("880", "TXT_KEY_AD"),
("895", "TXT_KEY_AD"),
("910", "TXT_KEY_AD"),
("966", "TXT_KEY_AD"),
("1016", "TXT_KEY_AD"),
("1066", "TXT_KEY_AD"),
("1139", "TXT_KEY_AD"),
("1236", "TXT_KEY_AD"),
("1282", "TXT_KEY_AD"),
("1359", "TXT_KEY_AD"),
("1380", "TXT_KEY_AD"),
("1523", "TXT_KEY_AD"),
("1581", "TXT_KEY_AD"),
("500", "TXT_KEY_AD")
)

# starting locations coordinates
tCapitals = (
(81, 24), #tConstantinople, Byzantium
(44, 46), #tParis, France
(97, 10), #tDamascus, Arabia
(78, 29), #tPreslav, Bulgaria
(30, 23), #tCordoba, Cordoba
(59, 57), #tRoskilde, Norse
(56, 35), #tVenice, Venezia
(47, 41), #tDijon, Burgundy
(53, 46), #tFrankfurt, Germany
(83, 45), #tKiev, Kiev
(66, 37), #tBuda, Hungary
(27, 32), #tLeon, Spain
(65, 49), #tPoznan, Poland
(50, 34), #tGenoa, Genoa
(41, 52), #tLondon, England
(21, 25), #tLisboa, Portugal
(75, 53), #tVilnius, Lithuania
(62, 40), #tWien, Austria
(78, 22), #tGallipoli, Ottomans
#(81, 22), #tBursa, Ottomans		#Bursa is too close to Constaninople
(91, 56), #tMoscow, Moscow
(66, 64), #tStockholm, Sweden
(49, 52), #tAmsterdam, Dutch
(56, 27)  #tRome, Pope
)

tStartingWorkers = (
0, #tByzantium
0, #tFrance
1, #tArabia
1, #tBulgaria
2, #tCordoba
2, #tNorse
2, #tVenice
2, #tBurgundy
3, #tGermany
3, #tKiev
3, #tHungary
3, #tSpain
3, #tPoland
3, #tGenoa
3, #tEngland
3, #tPortugal
3, #tLithuania
4, #tAustria
4, #tTurkey
4, #tMoscow
4, #tSweden
4, #tDutch
0  #tRome
)

#for minor civs
tReserveCapitals = (
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
(),
)

tNewCapitals = (  #for RiseAndFall
((81, 24),(81, 24)), #tByzantium: Constantinople
((44, 46),(44, 46)), #tFrance: Paris
((83, 3),(84, 3),(84, 4)), #tArabia: Damascus --> Alexandria (best Egyptian city)
((78, 29),(78, 29)), #tBulgaria: Preslav
((48, 16),(50, 18)), #tCordoba: Cordoba --> Hafsids at Tunis
((59, 57),(59, 57)), #tNorse: Roskilde
((56, 35),(56, 35)), #tVenezia: Venice
((47, 41),(47, 41)), #tBurgundy: Dijon
((59, 49),(61, 50)), #tGermany: Frankfurt --> Berlin
((83, 45),(83, 45)), #tKiev: Kiev
((66, 37),(66, 37)), #tHungary: Buda
((30, 27),(31, 27),(31, 28),(32, 28)), #Spain: Leon --> Toledo or Madrid
((65, 49),(65, 49)), #tPoland: Poznan
((50, 34),(50, 34)), #tGenoa: Genoa
((41, 52),(41, 52)), #tEngland: London
((21, 25),(21, 25)), #tPortugal: Lisboa
((75, 53),(75, 53)), #tLithuania: Vilnius
((62, 40),(62, 40)), #tAustria: Wien
((78, 22),(78, 22)), #tTurkey, Gallipoli
((91, 56),(91, 56)), #tMoscow: Moscow
((66, 64),(66, 64)), #tSweden: Stockholm
((49, 52),(49, 52)), #tDutch: Amsterdam
((56, 27),(56, 27))  #tPope: Rome
)

#core areas (for RiseAndFall and Victory)

# 3Miro: tCoreArea and tNormalArea are misleading, TL is not TopLeft and BR is not BottomRight (unless the grid starts from 0,0 at TL and counts down as positive y direction)
#	TL is actually BottomLeft and BR is TopRight
#	Many functions reference those and there are search algorithm that I do not whant to change, so leave this with the comment on how to be used
#	Also Broader Area

tCoreAreasTL = ( #Core Area is initial spawn location, no longer relevant for stability
(66,14),   #Byzantium
(42,43),   #Franks
(92,0),    #Arabs
(74,27),   #Bulgaria
(24,19),   #Cordoba
(53,55),   #Norse
(55,33),   #Venice
(44,32),   #Burgundy
(51,40),   #Germany
(79,42),   #Kiev
(64,33),   #Hungary
(25,30),   #Spain
(64,43),   #Poland
(49,27),   #Genoa
(37,48),   #England
(21,24),   #Portugal
(70,50),   #Lithuania
(59,37),   #Austria
(76,16),   #Ottomans
(83,54),   #Moscow
(61,59),   #Sweden
(46,50),   #Netherlands
(54,25)	   #Pope
)

tCoreAreasBR = (
(84,26),   #Byzantium
(46,47),   #Franks
(99,12),   #Arabs
(80,30),   #Bulgaria
(37,28),   #Cordoba
(60,67),   #Norse
(59,36),   #Venice
(48,42),   #Burgundy
(58,50),   #Germany
(88,50),   #Kiev		AbsintheRed: Kursk shouldn't flip to them, rather they should easily conquer it in the first few turns
(73,39),   #Hungary
(32,36),   #Spain
(70,50),   #Poland
(52,35),   #Genoa
(43,60),   #England
(24,32),   #Portugal
(77,59),   #Lithuania
(62,44),   #Austria
(84,22),   #Ottomans
(97,66),   #Moscow
(68,71),   #Sweden
(52,55),   #Netherlands
(58,29)	   #Pope
)


tExceptions = (  #for RiseAndFall. These are (badly named) extra squares used in spawn.
(), #Byzantium
(), #Frankia
(), #Arabia
(), #Bulgaria
((26,15),(26,16),(26,17),(26,18),(27,15),(27,16),(27,17),(27,18),(28,15),(28,16),(28,17),(28,18),(29,15),(29,16),(29,17),(29,18)), #Cordoba
((61,56),(61,57),(61,58),(61,59),(61,60),(62,57),(62,58),(62,59)), #Norse
((60,33),(60,34),(60,35)), #Venice
((49,39),(49,40),(49,41),(49,42)), #Burgundy
(), #Germany
(), #Kiev
(), #Hungary
(), #Spain
((63,46),(63,47),(63,48),(63,49),(63,50)), #Poland
(), #Genoa
((37,46),(37,47),(38,46),(38,47),(39,46),(39,47),(40,46),(40,47),(41,46),(41,47),(42,47)), #England		3Miro: Calais shouldn't flip to them on spawn
((25,27),(25,28),(25,29),(25,30),(25,31)), #Portugal
(), #Lithuania
((60,36),(61,36),(62,36)), #Austria
((76,23),(77,23),(78,23),(79,23)), #Ottomans
(), #Moscow
((60,60),(60,61),(60,62),(60,63),(69,65),(69,66),(69,67),(69,68),(70,65),(70,66),(70,67),(70,68),(71,65),(71,66),(71,67),(71,68),(72,65),(72,66),(72,67),(72,68)), #Sweden
((46,49),(47,49),(48,49),(49,49),(50,49)), #Dutch
()  #Pope
)

#normal areas

tNormalAreasTL = ( #These areas are typically used for resurrection.
(66,13),   #Byzantium
(33,32),   #Franks
(53,0),    #Arabs
(72,27),   #Bulgaria
(43,8),    #Cordoba
(53,56),   #Norse
(54,32),   #Venice
(45,32),   #Burgundy
(51,43),   #Germany
(78,41),   #Kiev
(63,33),   #Hungary
(25,18),   #Spain
(63,43),   #Poland
(49,22),   #Genoa
(32,50),   #England
(21,21),   #Portugal
(69,51),   #Lithuania
(57,36),   #Austria
(76,14),   #Turks
(83,51),   #Moscow
(60,59),   #Sweden
(47,50),   #Netherlands
(54,25)	   #Pope
)

tNormalAreasBR = (
(75,24),   #Byzantium
(44,46),   #Franks
(99,11),   #Arabs
(80,31),   #Bulgaria
(52,19),   #Cordoba
(59,71),   #Norse
(60,37),   #Venice
(49,43),   #Burgundy
(61,54),   #Germany
(91,50),   #Kiev
(77,41),   #Hungary
(42,36),   #Spain
(77,50),   #Poland
(52,36),   #Genoa
(43,71),   #England
(25,32),   #Portugal
(82,60),   #Lithuania
(63,42),   #Austria
(98,27),   #Turks
(98,71),   #Moscow
(68,71),   #Sweden
(52,54),   #Netherlands
(58,29)	   #Pope
)


tNormalAreasSubtract = (  #These are squares subtracted from normal areas
(), #Byzantium
((33,32),(33,33),(33,34),(33,35),(33,36),(34,32),(34,33),(34,34),(34,35),(35,32),(35,33),(35,34),(36,32),(36,33),(37,32),(38,32)), #Frankia
((73,10),(74,10),(75,10),(76,10),(87,10),(87,11),(88,10),(88,11),(89,11)), #Arabia
(), #Bulgaria
(), #Cordoba
(), #Norse
((54,32),(54,33),(54,34),(55,32),(55,33),(55,34),(56,32),(56,33),(56,34),(57,32),(57,33),(58,32),(59,37),(60,36),(60,37)), #Venice
((49,32),(49,33),(49,34),(49,35),(49,36)), #Burgundy
((52,51),(52,52),(52,53),(52,54),(51,51),(51,52),(51,53),(51,54)), #Germany
((87,41),(88,41),(89,41),(90,41),(91,41)), #Kiev
((63,39),(63,40),(63,41),(63,42),(64,41),(64,42),(75,41),(76,40),(76,41),(77,39),(77,40),(77,41)), #Hungary
((25,27),(25,28),(25,29),(25,30),(25,31),(34,36),(35,35),(35,36),(36,34),(36,35),(36,36),(37,33),(37,34),(37,35),(37,36),(38,33),(38,34),(38,35),(38,36),(39,32),(39,33),(39,34),(39,35),(39,36),(40,32),(40,33),(40,34),(40,35),(40,36),(41,31),(41,32),(41,33),(41,34),(41,35),(41,36),(42,31),(42,32),(42,33),(42,34),(42,35),(42,36)), #Spain
((63,43),(63,44),(63,45),(64,43),(64,44),(65,43)), #Poland
(), #Genoa
((32,55),(32,56),(32,57),(32,58),(32,59),(32,60),(32,61),(32,62),(32,63),(32,64),(33,56),(33,57),(33,58),(33,59),(33,60),(33,61),(33,62),(33,63)), #England
((25,21),(25,22),(25,23),(25,24),(25,25),(25,26),(25,32)), #Portugal
((69,51),(69,52),(69,53),(69,54),(70,51),(70,52),(70,53),(71,51),(71,52),(72,51)), #Lithuania
((57,36),(57,37),(58,36),(58,37),(59,36),(63,36),(63,37),(63,38)), #Austria
((76,27),(77,27),(78,27),(79,27),(80,27)), #Turkey
(), #Moscow
(), #Sweden
((51,50),(52,50)), #Dutch
()
)


# broader areas coordinates (top left and bottom right) (for RiseAndFall)
# 3Miro: see core area comment
# Sedna17: Currently unused?
tBroaderAreasTL = (
(68, 14), #Byzantium
(39, 41), #France
(92,  7), #Arabia
(71, 28), #Bulgaria
(24, 23), #Cordoba
(52, 53), #Norse
(52, 29), #tVenice
(42, 36), #Burgundy
(49, 41), #tGermany
(81, 37), #tKiev
(64, 27), #tHungary
(23, 31), #Spain
(64, 42), #tPoland
(45, 29), #tGenoa
(38, 49), #tLondon, England
(17, 27), #tLisboa, Portugal
(68, 45), #Lithuania
(56, 35), #tAustria
(83, 17), #tTurkey
(83, 51), #tMoscow
(62, 59), #tSweden
(44, 47), #tDutch
(54, 25)  #Pope
)

tBroaderAreasBR = (
(83, 27), #Byzantium
(49, 51), #France
(99, 15), #Arabia
(80, 31), #Bulgaria
(34, 33), #Cordoba
(62, 63), #Norse
(62, 39), #tVenice
(52, 46), #Burgundy
(58, 51), #tGermany
(91, 47), #tKiev
(74, 37), #tHungary
(33, 41), #Spain
(74, 52), #tPoland
(55, 39), #tGenoa
(48, 59), #tLondon, England
(27, 37), #tLisboa, Portugal
(82, 64), #Lithuania
(66, 45), #tAustria
(93, 27), #tTurkey
(93, 61), #tMoscow
(72, 69), #tSweden
(54, 57), #tDutch
(58, 29)  #Pope
)

# visible areas:
tVisible = (
( (64,0,99,34),(49,1,63,38),(24,17,48,36), ), # Byzantium
( (35,31,52,51),(49,26,59,38), ), # France
( (79,0,89,6),(90,0,99,22), ), # Arabia
( (69,24,81,31),(79,31,99,41), ), # Bulgaria
( (14,17,39,33),(40,0,59,20),(60,0,95,7), ), # Cordoba
( (52,55,68,66), ), # Norse
( (47,14,59,38),(60,18,63,35),(64,18,68,29), ), # Venice
( (35,31,52,51),(49,26,59,38), ), # Burgundy
( (35,33,48,51),(49,27,63,55), ), # Germany
( (77,24,82,40),(83,31,89,46),(79,41,92,49) ), # Kiev
( (58,31,82,43), ), # Hungary
( (20,23,36,41),(37,30,48,50),(49,26,59,38), ), # Spain
( (57,36,76,55),(77,40,99,46), ), # Poland
( (33,20,63,37),(64,9,82,28), ), # Genoa
( (30,51,46,68),(35,46,46,50), ), # England
( (18,23,36,42), ), # Portugal
( (57,36,76,55),(77,40,99,46),(70,33,99,58), ), # Lithuania
( (35,33,48,51),(49,27,63,55), ), # Austria
( (77,14,99,27),(93,5,99,13), ), # Turkey
( (70,33,99,58),(74,59,99,69), ), # Moscow
( (52,53,74,72), ), # Sweden
( (42,42,65,66), ), # Dutch
( (39,12,73,44), ), # Pope
)


# 3Miro: Initial Wars, note only the upper triangle of the array is valid, the lower should be all zeros
tWarAtSpawn = (
#Byz Fra Ara Bul Cor Nor Ven Bur Ger Kie Hun Spa Pol Gen Eng Por Lit Aus Tur Mos Swe Dut Pop In1 In2 In3 In4
( 0,  0, 90, 90,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 90,  0,  0,  0,  0,  0,  0,  0,  0, ), #Byz
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 60,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Fra
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 70,  0,  0,  0,  0,  0,  0,  0,  0, ), #Ara
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 70,  0,  0,  0,  0,  0,  0,  0,  0, ), #Bul
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 90,  0,  0,  0, 90,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Cor
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 80,  0,  0,  0,  0,  0,  0, ), #Nor
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Ven
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Bur
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Ger
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Kie
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Hun
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 60,  0,  0,  0,  0,  0, ), #Spa
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Pol
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Gen
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Eng
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Por
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Lit
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Aus
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 50, 50, 50, 50, ), #Tur
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Mos
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Swe
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Dut
)

iMercPromotion = 48

#Mercenaries. Higher number = less likely to hire
tHire = (
10, #Byzantium
30, #Frankia
50, #Arabia
10, #Bulgaria
50, #Cordoba
10, #Norse
30, #Venezia
10, #Burgundy
70, #Germany
40, #Kiev
10, #Hungary
40, #Spain
60, #Poland
30, #Genoa
70, #England
40, #Portugal
20, #Lithuania
20, #Austria
80, #Turkey
60, #Moscow
40, #Sweden
30, #Dutch
80, #Pope
50, #Indep1
50, #Indep2
50, #Indep3
50, #Indep4
50  #Barb (probably not needed)
)


#AIWars
tAggressionLevel = (
1, #Byzantium
1, #Frankia
2, #Arabia
2, #Bulgaria
1, #Cordoba
2, #Norse
0, #Venezia
0, #Burgundy
1, #Germany
1, #Kiev
2, #Hungary
2, #Spain
0, #Poland
0, #Genoa
1, #England
2, #Portugal
1, #Lithuania
1, #Austria
2, #Turkey
1, #Moscow
2, #Sweden
0, #Dutch
0  #Pope
)


#War during rise of new civs. Higher number means less chance for war
tAIStopBirthThreshold = (
30, #Byzantium
60, #Frankia
50, #Arabia
70, #Bulgaria
10, #Cordoba
70, #Norse
30, #Venezia
20, #Burgundy
80, #Germany
80, #Kiev
80, #Hungary
80, #Spain
40, #Poland
40, #Genoa
80, #England
30, #Portugal
40, #Lithuania
30, #Austria
80, #Turkey
70, #Moscow
60, #Sweden
20, #Dutch
90, #Pope
0, #Indep1
0, #Indep2
0, #Indep3
0, #Indep4
0  #Barb (probably do not need indies and barbs here.)
)


#RiseAndFall. This is one place to tune frequency of resurrections.
tResurrectionProb = (
20, #Byzantium
80, #Frankia
60, #Arabia
30, #Bulgaria
50, #Cordoba
60, #Norse
20, #Venezia
10, #Burgundy
70, #Germany
20, #Kiev
50, #Hungary
80, #Spain
60, #Poland
10, #Genoa
70, #England
60, #Portugal
40, #Lithuania
70, #Austria
60, #Turkey
80, #Moscow
70, #Sweden
60, #Dutch
90  #Pope
)

#Sedna17 Respawn: These dates are the most likely times for each civ to have its special opportunity to respawn
tRespawnTime = (
999, #Byzantium -- no special respawn
350, #Frankia 1600 -- France united to modern borders + start of Bourbon royal line
190, #Arabia 1170 -- Ayyubid dynasty from Egypt to cause problems for Crusaders
195, #Bulgaria 1185 -- Second Bulgarian empire
#174, #Cordoba 1122 -- Almohads, better timing than Almoravids
215, #Cordoba 1229 (give or take, it is semi-random anyway) 3Miro: we use Cordoba player to respawn as Hafsid in Tunisia
265, #Norse 1395 -- Kalmar Union
999, #Venezia -- no special respawn
245, #Burgundy 1335 -- so they can participate in 100 years war and act as Valois Duchy of Burgundy
401, #Germany 1701 -- Prussia
999, #Kiev -- no special respawn
393, #Hungary 1686 -- reconquest of Buda from the Ottomans
290, #Spain 1467 -- Union of Castile/Aragon and ready for colonies
999, #Poland -- no special respawn
999, #Genoa -- no special respawn
380, #England 1660 -- Restoration of Monarchy (also leading up to Scottish Union)
267, #Portugal 1400 -- Make sure Portugal is around for colonies
999, #Lithuania -- no special respawn
313, #Austria 1526 -- Battle of Mohacs, start of Habsburg influence in NW Hungary
294, #Turkey 1482 -- End of Mehmed II conquest.
999, #Moscow -- no special respawn
999, #Sweden -- no special respawn
999, #Dutch -- no special respawn
999  #Pope -- no special respawn
)


#Congresses. # 3Miro: there is no congress, maybe I should remove this
tPatienceThreshold = (
30, #Byzantium
30, #Frankia
30, #Arabia
30, #Bulgaria
30, #Cordoba
30, #Norse
30, #Venezia
30, #Burgundy
30, #Germany
30, #Kiev
30, #Hungary
30, #Spain
30, #Poland
30, #Genoa
30, #England
30, #Portugal
30, #Lithuania
30, #Austria
30, #Turkey
30, #Moscow
30, #Sweden
30  #Dutch
)


# religion spread modifiers:
tReligionSpreadFactor = ( # PROT, ISL, CATH, ORTH, JUD
(100,  50,  70, 150,  10), #Byzantium
(150,  20, 250,  70,  10), #France
( 20, 350,  50,  10,  10), #Arabia
(100,  50, 100, 350,  10), #Bulgaria
( 50, 250, 100,  20,  10), #Cordoba
(250,  50, 100, 150,  10), #Norse
( 90,  50, 200,  30,  10), #tVenezia
(150,  20, 150,  70,  10), #Burgundy
(450,  20, 250,  20,  10), #tGermany
( 90,  90,  90, 250,  10), #tKiev
(250,  80, 150, 100,  10), #tHungary
(100,  20, 200,  20,  10), #Spain
(200, 100, 400, 200,  10), #tPoland
(190,  50, 250,  30,  10), #tGenoa
(450,  20, 100,  20,  10), #tEngland
(200,  80, 250,  20,  10), #tPortugal
(80,   80,  80,  80,  80), #tLithuania
(200,  20, 250,  20,  10), #tAustria
( 20, 350,  80,  80,  10), #tTurkey
(100,  20, 100, 250,  10), #tMoscow
(550,  20, 100, 100,  10), #tSweden
(550,  20,  90,  20,  10), #tDutch
( 10,  20, 500,  10,  10), #Pope
(250, 100, 100, 100,  10), #Indy1
(250, 100, 100, 100,  10), #Indy2
(250, 100, 100, 100,  10), #Indy3
(250, 100, 100, 100,  10), #Indy4
( 20,  20,  20,  20,  10)  #Barb
)


# The AI will persecute religions in this order, depending on its own state religion (one row per religion)
tPersecutionOrder = (
	(xml.iCatholicism, xml.iIslam, xml.iOrthodoxy, xml.iJudaism),			# Protestantism
	(xml.iCatholicism, xml.iOrthodoxy, xml.iProtestantism, xml.iJudaism),	# Islam
	(xml.iIslam, xml.iProtestantism, xml.iJudaism, xml.iOrthodoxy),			# Catholicism
	(xml.iIslam, xml.iJudaism, xml.iCatholicism, xml.iProtestantism),		# Orhodoxy
	(xml.iIslam, xml.iProtestantism, xml.iOrthodoxy, xml.iCatholicism),		# Judaism
)


# 100 and 80: don't purge any religions; 60: purge islam if christian, and all christian religions if muslim; 40: also judaism; 20: all but state religion
tReligiousTolerance = (
60, #Byzantium
40, #Frankia
60, #Arabia
40, #Bulgaria
80, #Cordoba
60, #Norse
40, #Venezia
20, #Burgundy
20, #Germany
40, #Kiev
60, #Hungary
20, #Spain
80, #Poland
20, #Genoa
40, #England
20, #Portugal
80, #Lithuania
20, #Austria
20, #Turkey
40, #Moscow
60, #Sweden
40, #Dutch
20, #Pope
100, #Indy1
100, #Indy2
100, #Indy3
100, #Indy4
100, #Barbarian
)


#Stability Parameters
iParCities3 = 0
iParCitiesE = 1
iParCivics3 = 2
iParCivics1 = 3
iParCivicsE = 4
iParDiplomacy3 = 5
iParDiplomacyE = 6
iParEconomy3 = 7
iParEconomy1 = 8
iParEconomyE = 9
iParExpansion3 = 10
iParExpansion1 = 11
iParExpansionE = 12
iNumStabilityParameters = 13


#Plague
iImmunity = 20


#Positions on the Colony map for "home" original flags
home_positions_xy = [
(578,179), #iByzantium = 0
(480,152), #iFrankia = 1
(614,212), #iArabia = 2
(567,166), #iBulgaria = 3
(455,195), #iCordoba = 4
(515,118), #iNorse = 5
(518,157), #iVenice = 6
(490,160), #iBurgundy = 7
(510,140), #iGermany = 8
(590,140), #iKiev = 9
(550,155), #iHungary = 10
(460,180), #iSpain = 11
(540,130), #iPoland = 12
(503,165), #iGenoa = 13
(473,132), #iEngland = 14
(441,190), #iPortugal = 15
(556,119), #iLithuania = 16
(535,150), #iAustria = 17
(590,195), #iTurkey = 18
(595,110), #iMoscow = 19
(531, 92), #iSweden = 20
(492,131), #iDutch = 21
]

#Positions on the Colony map where to display colonies
colony_positions_xy=[
(0,0), #Dummy slots for non-colony projects
(0,0),
(0,0),
(275,150), #Vinland
(480,335), # GoldCoast
(440,335), # IvoryCoast
(145,265), # Cuba
(290,410), #Brazil
(160,110), #Hudson
(170,210), #Virginia
(875,225), #China
(760,260), #India
(930,360), #East Indies
(870,320), #Malaysia
(560,510), #CapeTown
(610,390), #EastAfrica
(60,260),  #Aztecs
(170,420), #Inca
(185,280), #Hispaniola
(245,120), #Quebec
(200,180), #New England
(155,285), #Jamaica
(130,325), #Panama
(110,220), #Louisiana
(960,320), #Philipines
]


tLeaders = (		#First has to be the primary leader (the one that appears on the civ selection screen). Can be changed in the WB file (AbsintheRed)
(xml.iJustinian,),
(xml.iCharlemagne, xml.iJoan, xml.iLouis_Xiv),
(xml.iAbuBakr, xml.iSaladin),
(xml.iSimeon, xml.iIvan_Asen),
(xml.iAbdarRahman, xml.iAbuYusufYaqub),
(xml.iHarald_Hardrada, xml.iHaakon_Iv, xml.iChristian_Iv),
(xml.iDandolo, xml.iAndrea_Dandolo),
(xml.iPhilip_the_Bold,),
(xml.iBarbarossa, xml.iFrederick),
(xml.iYaroslav,),
(xml.iStephen, xml.iMatthias),
(xml.iIsabella, xml.iPhilip_Ii),
(xml.iCasimir, xml.iSobieski),
(xml.iSimone,),
(xml.iWilliam, xml.iElizabeth, xml.iGeorge_Iii),
(xml.iAfonso, xml.iJoao, xml.iMaria_Ii),
(xml.iMindaugas, xml.iVytautas),
(xml.iMaximilian, xml.iMaria_Theresa),
(xml.iMehmed, xml.iSuleiman),
(xml.iIvan_Iv, xml.iPeter, xml.iCatherine),
(xml.iGustavus, xml.iKarl_Xii),
(xml.iWillem_Van_Oranje,),
(xml.iThe_Pope,)
)


tEarlyLeaders = (		#Don't have to be the same as the primary leader (AbsintheRed)
(xml.iJustinian),
(xml.iCharlemagne),
(xml.iAbuBakr),
(xml.iSimeon),
(xml.iAbdarRahman),
(xml.iHarald_Hardrada),
(xml.iDandolo),
(xml.iPhilip_the_Bold),
(xml.iBarbarossa),
(xml.iYaroslav),
(xml.iStephen),
(xml.iIsabella),
(xml.iCasimir),
(xml.iSimone),
(xml.iWilliam),
(xml.iAfonso),
(xml.iMindaugas),
(xml.iMaximilian),
(xml.iMehmed),
(xml.iIvan_Iv),
(xml.iGustavus),
(xml.iWillem_Van_Oranje),
(xml.iThe_Pope)
)


tLateLeaders = (		#All switch dates up to 200 years earlier because the switch is triggered after a few years (date, percentage, era)
(xml.iJustinian,),
(xml.iJoan, xml.i1160AD, 10, 2, xml.iLouis_Xiv, xml.i1452AD, 25, 3),
(xml.iSaladin, xml.i1160AD, 25, 2),
(xml.iIvan_Asen, xml.i1101AD, 10, 2),
(xml.iAbuYusufYaqub, xml.i1101AD, 10, 2),
(xml.iHaakon_Iv, xml.i1160AD, 25, 2, xml.iChristian_Iv, xml.i1520AD, 5, 3),
(xml.iAndrea_Dandolo, xml.i1200AD, 10, 2),
(xml.iPhilip_the_Bold,),
(xml.iFrederick, xml.i1520AD, 5, 3),
(xml.iYaroslav,),
(xml.iMatthias, xml.i1452AD, 5, 3),
(xml.iPhilip_Ii, xml.i1520AD, 10, 3),
(xml.iSobieski, xml.i1570AD, 10, 3),
(xml.iSimone,),
(xml.iElizabeth, xml.i1452AD, 10, 3, xml.iGeorge_Iii, xml.i1700AD, 10, 3),
(xml.iJoao, xml.i1419AD, 10, 3, xml.iMaria_Ii, xml.i1700AD, 10, 3),
(xml.iVytautas,xml.i1377AD,10,3),
(xml.iMaria_Theresa, xml.i1700AD, 25, 3),
(xml.iSuleiman, xml.i1520AD, 15, 3),
(xml.iPeter, xml.i1570AD, 10, 3, xml.iCatherine, xml.i1700AD, 25, 3),
(xml.iKarl_Xii, xml.i1570AD, 10, 3),
(xml.iWillem_Van_Oranje,),
(xml.iThe_Pope,)
)


# 3Miro: UP begins here
#iUP_Culture = 0
#iUP_Emperor = 1
#iUP_Stability = 2
#iUP_Faith = 3
#iUP_Khan = 4
#iUP_Medicine = 5
#iUP_Inquisition = 6
#iUP_Sea = 7
#iUP_Trade = 8
#iUP_Growth = 9
#iUP_Tolerance = 10
#iUP_Industry = 11
#iUP_GoldenLiberty = 12
#iUP_EndlessLand = 13
#iUP_Mercenaries = 14
#iUP_Workshops = 15
#iUP_Alliances = 17
#iUP_Conscription = 18
#iUP_Formation = 19
#iUP_Commerce = 20
# alliances and Endless land could be fixed in diplo relations and maintenance


iUP_Happiness = 0			# happiness bonus
iUP_PerCityCommerce = 1		# bonus of commerse per city
iUP_CityTileYield = 2		# bonus on yield of the city tile
iUP_ReligiousTolerance = 3	# no instability from foreign religion
iUP_CulturalTolerance = 4	# no unhappiness from foreign culture
iUP_CommercePercent = 5		# global bonus to specific type of commerce
iUP_UnitProduction = 6		# after specific tech, faster unit production
iUP_EnableCivic = 7			# always enable some civics (also use the WB)
iUP_TradeRoutes = 8			# add some trade routes (sync with GlobalDefines.xml for max trade routes)
iUP_ImprovementBonus = 9	# chnage the yield of a specific improvement
iUP_PromotionI = 10			# give a promotion to all units for which it is valid
iUP_PromotionII = 11		# give a promotion to all units regardless if it is valid
iUP_CanEnterTerrain = 12	# all unit can enter some terrain type
iUP_NoResistance = 13		# no resistance from conquering cities
iUP_Conscription = 14		# can draft from cities with foreign culture
iUP_Inquisition = 15		# no instability from religious prosecution
iUP_Emperor = 16			# no civil war and no secession in the core (Python only)
iUP_Faith = 17				# state religion spreads to newly accuired cities (found/trade/conquest) with a temple (Python only)
iUP_Mercenaries = 18		# halves the cost of mercenaries (Python only - Mercenaries)
iUP_LandStability = 19		# no penalty from owning unstable land (Python only)
iUP_Discovery = 20			# lower cost of a block of projects
iUP_EndlessLand = 21		# lower civic cost assosiated with cities
iUP_ForeignSea = 22			# allows the ships to enter foreign sea territory (Dutch UP from RFC)
iUP_Pious = 23				# increase the gain (and loss) of Faith Points
iUP_PaganCulture = 24		# give bonus to culure if no state religion is present
iUP_PaganHappy = 25			# give bonus to happyness if no state religion is present
iUP_StabilityConquestBoost = 26		# if stability is < 0, then get +1 stability on Conquest
iUP_StabilitySettler = 27			# don't lose stability from founding cities in Outer and None Provinces
iUP_StabilityPlaceholder1 = 28		# does nothing
iUP_StabilityPlaceholder2 = 29		# does nothing
iUP_Janissary = 30					# free units for foreign religions (Python only)


iFP_Stability = 0		# stability bonus
iFP_Civic = 1			# lower civic upkeep
iFP_Growth = 2			# faster population growth
iFP_Units = 3			# lower production cost for units
iFP_Science = 4			# lower beaker cost for new techs
iFP_Production = 5		# lower cost for Wonders and Projects
iFP_Displomacy = 6		# diplomacy boost

# Saint section
iSaintBenefit = 10		# number of Faith points generated by a saint

# Crusade section / Towns
iNumCrusades = 5
iJerusalem = ( 93, 5 )


# Province Status
iProvinceOwn = 5      # own every tile
iProvinceConquer = 4  # own every city (capture or settle) or own every tile
iProvinceDominate = 3 # 2*sum of population + owned tiles is more for you than the sum total of everyone else (true if conquer is true)
iProvinceLost = 2     # you have no cities and others have cities in it

# ProvinceTypes
iProvinceNone      = 0 # this is the default, use it for everything too far away to be considered
iProvinceDesired   = 1 # for AI purposes, same as outer, just lower aggession flag
iProvinceOuter     = 2 # small stability hit on owning
iProvincePotential = 3 # changes to Core or Natural as soon as conquered
iProvinceNatural   = 4 # stable, small penalty for not conquering it
iProvinceCore      = 5 # stable, large penalty for not conquering it
iNumProvinceTypes  = 6

# special parameters 10 per player (picklefree)
iIsHasStephansdom = 0 # Stability parameter in Python
iIsHasEscorial    = 1 # Stability parameter in Python
iMercCostPerTurn  = 2 # Mercenaries
iJanissaryPoints  = 3 # Janissary points

# Stability Cathegories
iCathegoryCities = 0
iCathegoryCivics = 1
iCathegoryEconomy = 2
iCathegoryExpansion = 3
