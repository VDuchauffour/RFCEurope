# Rhye's and Fall of Civilization - Constants

# globals

#from CvPythonExtensions import *
#gc = CyGlobalContext()

import XMLConsts as xml

l0Array =       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 3Miro for stability, counts the cities for each player
l0ArrayActive = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
l0ArrayTotal =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # this is just a dummy array

lm1Array =      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

# 3Miro: map size entered here
iMapMaxX = 100
iMapMaxY = 73

#### Chronological order
# Byzantium   i500AD
# France      i500AD
# Arabia      i635AD
# Bulgaria    i680AD
# Cordoba     i711AD
# Norse       i780AD
# Venice      i810AD
# Burgundy    i843AD
# Germany     i858AD
# Kiev        i880AD
# Hungary     i895AD
# Spain       i910AD
# Poland      i966AD
# Genoa       i1016AD
# England     i1066AD
# Portugal    i1139AD
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
[iBulgaria,iArabia],	#Byzantium
[iBurgundy,iEngland],	#Frankia
[iByzantium],			#Arabia
[iByzantium,iHungary,iKiev],	#Bulgaria
[iSpain,iPortugal],		#Cordoba
[iSweden],			#Norse
[iGenoa,iGermany,iAustria,iHungary,iPope],		#Venecia
[iFrankia,iDutch,iGermany],		#Burgundy
[iBurgundy,iDutch,iAustria,iVenecia,iGenoa,iPoland,iHungary],	#Germany
[iBulgaria,iMoscow,iPoland],		#Kiev
[iBulgaria,iVenecia,iPoland,iGermany,iAustria],			#Hungary
[iCordoba,iPortugal],	#Spain
[iGermany,iAustria,iHungary,iKiev,iMoscow],				#Poland
[iGermany,iVenecia,iBurgundy,iPope],	#Genoa
[iFrankia,iDutch],			#England
[iSpain,iCordoba],			#Portugal
[iKiev,iPoland],		#Lithuania
[iGermany,iHungary,iPoland,iVenecia],	#Austria
[iByzantium,iArabia],			#Turkey
[iKiev,iPoland],		#Moscow
[iNorse],				#Sweden
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
[iCordoba], #Venecia
[], #Burgundy
[], #Germany
[iBulgaria], #Kiev
[iBulgaria], #Hungary
[iCordoba], #Spain
[iGermany,iKiev], #Poland
[iVenecia,iGermany,iCordoba], #Genoa
[iFrankia], #England
[iSpain,iCordoba], #Portugal
[iPoland], #Portugal
[iGermany,iHungary,iVenecia,iGenoa], #Austria
[iByzantium,iBulgaria,iCordoba,iArabia], #Turkey
[iKiev,iPoland], #Moscow
[iNorse,iPoland,iMoscow], #Sweden
[iGermany,iFrankia], #Dutch
[] #Pope
]

# civ birth dates
tBirth = (
xml.i500AD, #500AD Byzantium
xml.i500AD, #500AD Frankia
xml.i635AD, #632AD Arabia
xml.i680AD, #680AD Bulgaria
xml.i711AD, #712AD Cordoba
xml.i780AD, #780AD Norse
xml.i810AD, #800AD Venecia
xml.i843AD, #843AD Burgundy
xml.i858AD, #858AD Germany
xml.i880AD, #864AD Kiev # There is an Autorun Bug, usually Kiev and Hungary play one extra turn (but not always)
xml.i895AD, #896AD Hungary # There is an Autorun Bug, usually Kiev and Hungary play one extra turn (but not always)
xml.i910AD, #910AD Spain
xml.i966AD, #966AD Poland
xml.i1016AD,#1020AD Genoa
xml.i1066AD,#1066AD England
xml.i1139AD,#1100AD Portugal
xml.i1236AD,#1236AD Lithuania
xml.i1282AD,#1282AD Austria
xml.i1359AD,#1359AD Turkey - turn 233 is normal time (Conquest of Adrianopolis)
xml.i1380AD,#1380AD Moscow
xml.i1523AD,#1523AD Sweden
xml.i1581AD,#1580AD Dutch - turn 340 is normal time
0,	#Pope
0,
0,
0,
0,
0
) # 3Miro: tBirth should finish with zeros for all minor civs (indeps, barbs and celts in original RFC)


tYear = ( # for Dawn of Man starting screen
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
(81, 25), #tConstantinople, Byzantium
(44, 46), #tParis, France
(97, 13), #tDamascus, Arabia
(77, 30), #tPreslav, Bulgaria
(28, 28), #tCordoba, Cordoba
(59, 57), #tRoskilde, Norse
(56, 35), #tVenice, Venezia
(47, 41), #tDijon, Burgundy
(54, 46), #tFrankfurt, Germany
(83, 45), #tKiev, Kiev
(66, 37), #tBuda, Hungary
(28, 37), #tLeon, Spain
(65, 49), #tPoznan, Poland
(50, 34), #tGenoa, Genoa
(43, 53), #tLondon, England
(22, 32), #tLisboa, Portugal
(75, 53), #tVilnius, Lithuania
(63, 39), #tWien, Austria
(79, 22), #tBursa, Turkey
(88, 56), #tMoscow, Moscow
(67, 64), #tStockholm, Sweden
(49, 52), #tAmsterdam, Dutch
(56, 27)  #tRome, Pope
) 

tStartingWorkers = (
0, #tByzantium
0, #tFrance
1, #tArabia
1, #tBulgaria
1, #tCordoba
2, #tNorse
2, #tVenecia
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
((81, 25),(81, 25)), #tByzantium: Constantinople
((44, 46),(44, 46)), #tFrance: Paris
((85, 4),(84, 3),(85, 3)), #tArabia: Damascus --> Alexandria (best Egyption city)
((77, 30),(77, 30)), #tBulgaria: Preslav
((48, 16),(50, 18)), #tCordoba: Cordoba --> Hafsids at Tunis
((59, 57),(59, 57)), #tNorse: Roskilde
((56, 35),(56, 35)), #tVenezia: Venice
((47, 41),(47, 41)), #tBurgundy: Dijon
((61, 49),(60, 48),(61, 48),(62, 48)), #tGermany: Frankfurt --> Berlin
((83, 45),(83, 45)), #tKiev: Kiev
((66, 37),(66, 37)), #tHungary: Buda
((28, 32),(28, 31),(28, 33),(27, 31)), #Spain: Leon --> Toledo (like Madrid)
((65, 49),(65, 49)), #tPoland: Poznan
((50, 34),(50, 34)), #tGenoa: Genoa
((43, 53),(43, 53)), #tEngland: London
((22, 32),(22, 32)), #tPortugal: Lisboa
((75, 53),(75, 53)), #tLithuania: Vilnius
((63, 39),(63, 39)), #tAustria: Wien
((79, 22),(79, 22)), #tTurkey: Bursa
((88, 56),(88, 56)), #tMoscow: Moscow
((67, 64),(67, 64)), #tSweden: Stockholm
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
(42,42),   #Franks
(93,1),    #Arabs
(74,28),   #Bulgaria
(25,18),   #Cordoba
(54,56),   #Norse
(56,33),   #Venice
(44,33),   #Burgundy
(52,40),   #Germany
(80,37),   #Kiev
(65,34),   #Hungary
(25,34),   #Spain
(64,44),   #Poland
(49,27),   #Genoa
(38,48),   #England
(21,29),   #Portugal
(71,48),   #Lithuania
(58,37),   #Austria
(76,16),   #Turks
(80,52),   #Moscow
(61,59),   #Sweden
(47,49),   #Netherlands
(54,25)	   #Pope
) 

tCoreAreasBR = (
(84,26),   #Byzantium
(46,47),   #Franks
(99,15),   #Arabs
(84,36),   #Bulgaria
(35,32),   #Cordoba
(59,65),   #Norse
(61,36),   #Venice
(48,42),   #Burgundy
(56,50),   #Germany
(91,48),   #Kiev
(71,39),   #Hungary
(33,40),   #Spain
(75,50),   #Poland
(53,35),   #Genoa
(44,58),   #England
(24,35),   #Portugal
(78,59),   #Lithuania
(64,43),   #Austria
(84,22),   #Turks
(95,68),   #Moscow
(66,69),   #Sweden
(52,57),   #Netherlands
(58,29)	   #Pope
)


tExceptions = (  #for RiseAndFall. These are (badly named) extra squares used in spawn.
(), #Byzantium
(), #Frankia
(), #Arabia
(), #Bulgaria
((24, 23), (24, 22), (24, 21), (24, 20), (24, 19), (23, 22), (23, 21), (23, 20)), #Cordoba
(), #Norse
(), #Venecia 
(), #Burgundy 
(), #Germany
(), #Kiev
(), #Hungary
(), #Spain
(), #Poland
(), #Genoa
((39, 47), (40, 47), (41, 47)), #England
((20, 29), (23, 36), (23, 37), (24, 36), (24, 37)), #Portugal
(), #Lithuania
((59, 44), (60, 44), (62, 44), (61, 44)), #Austria
((75,23),(75,24),(75,25),(75,26),(75,27),(76,23),(76,24),(76,25),(76,26),(76,27),(77,23),(77,24),(77,25),(77,26),(77,27),(78,23),(78,24),(78,25),(78,26),(78,27)), #Turkey
(), #Moscow
((60,59),(60,60),(60,61),(65,70),(66,70),(65,71),(66,71),(67,71),(68,71),(65,72),(66,72),(67,72),(68,72),(67,64),(67,65),(69,64),(70,66),(71,65),(71,66),(72,64),(72,65)), #Sweden
(), #Dutch
()  #Pope
)

#normal areas

tNormalAreasTL = ( #These areas are typically used for resurrection. Also used in stability and (maybe) for victory conditions
(66,14),   #Byzantium
(35,34),   #Franks
(48,1),    #Arabs
(73,28),   #Bulgaria
(44,9),    #Cordoba
(53,56),   #Norse
(56,33),   #Venice
(45,33),   #Burgundy
(52,44),   #Germany
(80,36),   #Kiev
(66,34),   #Hungary
(24,25),   #Spain
(64,43),   #Poland
(49,22),   #Genoa
(35,52),   #England
(20,28),   #Portugal
(68,45),   #Lithuania
(58,37),   #Austria
(76,13),   #Turks
(80,47),   #Moscow
(60,58),   #Sweden
(48,50),   #Netherlands
(54,25)	   #Pope
) 

tNormalAreasBR = (
(76,24),   #Byzantium
(44,49),   #Franks
(98,13),   #Arabs
(80,32),   #Bulgaria
(52,20),   #Cordoba
(59,71),   #Norse
(61,36),   #Venice
(49,44),   #Burgundy
(63,54),   #Germany
(97,43),   #Kiev
(78,40),   #Hungary
(41,40),   #Spain
(78,57),   #Poland
(52,35),   #Genoa
(45,67),   #England
(25,36),   #Portugal
(82,64),   #Lithuania
(65,42),   #Austria
(98,27),   #Turks
(98,71),   #Moscow
(69,71),   #Sweden
(51,54),   #Netherlands
(58,29)	   #Pope
) 


tNormalAreasSubtract = (  #These are squares subtracted from normal areas
(), #Byzantium
((35, 34), (36, 34), (37, 34), (38, 34), (35, 35), (36, 35), (37, 35), (35, 36), (35, 37)), #Frankia
((58,12),(72,10),(73,10),(74,10),(75,10),(78,11),(79,12),(88,11),(88,12),(89,11),(89,12),(90,12),(91,13)), #Arabia
(), #Bulgaria
(), #Cordoba
(), #Norse
(), #Venecia 
((49, 34), (49, 35),(49, 33)), #Burgundy
(), #Germany
(), #Kiev
(), #Hungary
((35, 40), (36, 40), (37, 40), (38, 40), (39, 40), (40, 40), (41, 39), (41, 40), (40, 39), (39, 39), (38, 39), (37, 39), (36, 39), (35, 39), (35, 38), (36, 38), (37, 38), (38, 38), (39, 38), (40, 38), (41, 38), (37, 37), (36, 37), (38, 37), (39, 37), (40, 37), (41, 37), (41, 36), (40, 36), (39, 36), (38, 36), (37, 36), (36, 36), (38, 35), (39, 35), (40, 35), (41, 35), (41, 34), (40, 34), (39, 34), (24, 36), (24, 35), (24, 34), (24, 33), (24, 32), (24, 31), (25, 36), (25, 35), (25, 34)), #Spain
(), #Poland
(), #Genoa
((35, 57), (35, 58), (36, 58), (35, 59), (36, 59)), #England
((24, 28), (25, 28), (24, 29), (25, 29), (24, 30), (25, 30), (25, 31), (25, 32), (25, 33)), #Portugal
(), #Lithuania
(), #Austria
(), #Turkey
(), #Moscow
(), #Sweden
(), #Dutch
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
(52, 29), #tVenecia
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
(62, 39), #tVenecia
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

# visiable areas:
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
30, #Venecia
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
0, #Venecia
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


#war during rise of new civs higher number means less war
tAIStopBirthThreshold = (
    30, #Byzantium
    60, #Frankia
    50, #Arabia
    70, #Bulgaria
    10, #Cordoba
    70, #Norse
    30, #Venecia
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
    20,  #Pope
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
20, #Venecia
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
999, #Venecia -- no special respawn
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
30, #Venecia
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
( 90,  50, 200,  30,  10), #tVenecia
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


iUP_Happiness = 0		# happiness bonus
iUP_PerCityCommerce = 1		# bonus of commerse per city
iUP_CityTileYield = 2		# bonus on yield of the city tile
iUP_ReligiousTolerance = 3	# no instability from foreign religion
iUP_CulturalTolerance = 4	# no unhappiness from foreign culture
iUP_CommercePercent = 5		# global bonus to specific type of commerce
iUP_UnitProduction = 6		# after specific tech, faster unit production
iUP_EnableCivic = 7		# always enable some civics (also use the WB)
iUP_TradeRoutes = 8		# add some trade routes (sync with GlobalDefines.xml for max trade routes)
iUP_ImprovementBonus = 9	# chnage the yield of a specific improvement
iUP_PromotionI = 10		# give a promotion to all units for which it is valid
iUP_PromotionII = 11		# give a promotion to all units regardless if it is valid
iUP_CanEnterTerrain = 12	# all unit can enter some terrain type
iUP_NoResistance = 13		# no resistance from conquering cities
iUP_Conscription = 14		# can draft from cities with foreign culture
iUP_Inquisition = 15		# no instability from religious prosecution
iUP_Emperor = 16		# no civil war and no secession in the core (Python only)
iUP_Faith = 17			# state religion spreads to newly accuired cities (found/trade/conquest) with a temple (Python only)
iUP_Mercenaries = 18		# halves the cost of mercenaries (Python only - Mercenaries)
iUP_LandStability = 19		# no penalty from owning unstable land (Python only)
iUP_Discovery = 20		# lower cost of a block of projects
iUP_EndlessLand = 21		# lower civic cost assosiated with cities
iUP_ForeignSea = 22		# allows the ships to enter foreign sea territory (Dutch UP from RFC)
iUP_Pious = 23			# increase the gain (and loss) of Faith Points
iUP_PaganCulture = 24           # give bonus to culure if no state religion is present
iUP_PaganHappy = 25             # give bonus to happyness if no state religion is present
iUP_StabilityConquestBoost = 26 # if stability is < 0, then get +1 stability on Conquest
iUP_StabilitySettler = 27       # don't lose stability from founding cities in Outer and None Provinces
iUP_StabilityPlaceholder1 = 28  # does nothing
iUP_StabilityPlaceholder2 = 29  # does nothing
iUP_Janissary = 30              # free units for foreign religions (Python only)


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
iJerusalem = ( 94, 6 )


# Province States
iProvinceOwn = 5      # own every tile
iProvinceConquer = 4  # own every city (capture or settle) or own every tile
iProvinceDominate = 3 # 2*sum of population + owned tiles is more for you than the sum total of everyone else (true if conquer is true)
iProvinceLost = 2     # you have no cities and others have cities in it

# ProvinceTypes
iProvinceNone      = 0 # this is the default, use it for everything too far away to be considered
iProvinceDesired   = 1 # for AI purposes, same as outer, just lower aggession flag
iProvinceOuter     = 2 # small stability hit on owning
iProvincePotential = 3 # changes to Home or Natural as soon as conquered
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
