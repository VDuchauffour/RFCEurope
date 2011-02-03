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

# initialise player variables to player IDs from WBS (this is the only part of the XML that will stay here)
iBurgundy = 0
iByzantium = 1
iFrankia = 2
iArabia = 3
iBulgaria = 4
iCordoba = 5
iSpain = 6
iNorse = 7
iVenecia = 8
iKiev = 9
iHungary = 10
iGermany = 11
iPoland = 12
iMoscow = 13
iGenoa = 14
iEngland = 15
iPortugal = 16
iAustria = 17
iTurkey = 18
iSweden = 19
iDutch = 20
iPope = 21
iNumPlayers = 22
iNumMajorPlayers = 22
iNumActivePlayers = 22
iIndependent = 22
iIndependent2 = 23
iIndependent3 = 24
iIndependent4 = 25
iNumTotalPlayers = 26
iBarbarian = 26
iNumTotalPlayersB = 27

iIndepStart = iIndependent # creates a block of independent civs
iIndepEnd = iIndependent4

#for Congresses and Victory
lCivGroups = [[iByzantium,iBulgaria,iKiev,iMoscow],  		#Eastern
		[iBurgundy,iHungary,iGermany,iPoland,iAustria],	#Central
		[iFrankia,iSpain,iEngland,iPortugal,iDutch],	#Atlantic
		[iArabia,iCordoba,iTurkey],			#Islamic
		[iGenoa,iVenecia, iPope],		 		#Italian
		[iNorse,iSweden]] 				#Scandinavian

lCivStabilityGroups = [[iByzantium,iBulgaria,iKiev,iMoscow],  #Eastern
			[iBurgundy,iHungary,iGermany,iPoland,iAustria],  		#Central
			[iFrankia,iSpain,iEngland,iPortugal,iDutch], 		#Atlantic
			[iArabia,iCordoba,iTurkey],		#Islamic
			[iGenoa,iVenecia, iPope], #Italian
			[iNorse,iSweden]]		#Norse

lCivBioOldWorld = [iByzantium, iBulgaria, iBurgundy, iArabia, iFrankia, iSpain, iCordoba, iNorse, iVenecia, iKiev, iHungary, \
		   iGermany, iPoland, iMoscow, iGenoa, iEngland, iPortugal, iAustria, iTurkey, iSweden, iDutch, iPope, \
                   iIndependent, iIndependent2, iBarbarian]
                   
lCivBioNewWorld = []


#for Victory and the handler
#tAmericasTL = (3, 0)
#tAmericasBR = (43, 63)


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
[iFrankia,iDutch,iGermany], #Burgundy
[iBulgaria,iArabia], #Byzantium
[iBurgundy,iEngland], #Frankia
[iByzantium], 		#Arabia
[iByzantium,iHungary,iKiev], #Bulgaria
[iSpain,iPortugal], 	#Cordoba
[iCordoba,iPortugal], 	#Spain
[iSweden],  		#Norse
[iGenoa,iGermany,iAustria,iHungary,iPope],  #Venecia
[iBulgaria,iMoscow,iPoland],  		#Kiev
[iBulgaria,iVenecia,iPoland,iGermany,iAustria],  		#Hungary
[iBurgundy,iDutch,iAustria,iVenecia,iGenoa,iPoland,iHungary],  #Germany
[iGermany,iAustria,iHungary,iKiev,iMoscow],  			#Poland
[iKiev,iPoland],  		#Moscow
[iGermany,iVenecia,iBurgundy,iPope],  #Genoa
[iFrankia,iDutch],  		#England
[iSpain,iCordoba],  		#Portugal
[iGermany,iHungary,iPoland,iVenecia],  	#Austria
[iByzantium,iArabia],  			#Turkey
[iNorse],  				#Sweden
[iGermany,iEngland,iBurgundy],   	#Dutch
[iVenecia, iGenoa]			#Pope
]

#for stability hit on spawn
lOlderNeighbours = [
[iFrankia], #Burgundy
[], #Byzantium
[], #Frankia
[iByzantium], #Arabia
[iByzantium], #Bulgaria
[], #Cordoba
[iCordoba], #Spain
[], #Norse
[iCordoba], #Venecia
[iBulgaria], #Kiev
[iBulgaria], #Hungary
[iHungary,iVenecia], #Germany
[iGermany,iKiev], #Poland
[iKiev,iPoland], #Moscow
[iVenecia,iGermany,iCordoba], #Genoa
[iFrankia], #England
[iSpain,iCordoba], #Portugal
[iGermany,iHungary,iVenecia,iGenoa], #Austria
[iByzantium,iBulgaria,iCordoba,iArabia], #Turkey
[iNorse,iPoland,iMoscow], #Sweden
[iGermany,iFrankia],  #Dutch
[] #Pope
]



# civ birth dates
tBirth = (
86, #843AD Burgundy
0,  #500AD Byzantium
0,  #500AD Frankia
33, #632AD Arabia
45, #680AD Bulgaria
53, #712AD Cordoba
104, #720AD Spain => 1083 (161) => 909
68, #770AD Norse
75, #800AD Venecia
91, #864AD Kiev # There is an Autorun Bug, usually Kiev and Hungary play one extra turn (but not always)
98, #896AD Hungary # There is an Autorun Bug, usually Kiev and Hungary play one extra turn (but not always)
88, # 843AD Germany
123,#970AD Poland
241,#1000AD Moscow => 1323
140,# 140 normally 1020AD Genoa
153,# 153 normally 1060AD England
167,#1100AD Portugal
187,#1160AD Austria
233,#1300AD Turkey - 233 is normal time
300,#1500AD Sweden
340,#1580AD Dutch 340 is normal time
0,	#Pope
0,
0,
0,
0,
0
) # 3Miro: tBirth should finish with zeros for all minor civs (indeps, barbs and celts in original RFC)


tYear = ( # for Dawn of Man starting screen
("844", "TXT_KEY_AD"),
("500", "TXT_KEY_AD"),
("500", "TXT_KEY_AD"),
("632", "TXT_KEY_AD"),
("680", "TXT_KEY_AD"),
("712", "TXT_KEY_AD"),
("909", "TXT_KEY_AD"),
("770", "TXT_KEY_AD"),
("800", "TXT_KEY_AD"),
("864", "TXT_KEY_AD"),
("895", "TXT_KEY_AD"),
("852", "TXT_KEY_AD"),
("970", "TXT_KEY_AD"),
("1323", "TXT_KEY_AD"),
("1020", "TXT_KEY_AD"),
("1060", "TXT_KEY_AD"),
("1100", "TXT_KEY_AD"),
("1160", "TXT_KEY_AD"),
("1300", "TXT_KEY_AD"),
("1500", "TXT_KEY_AD"),
("1580", "TXT_KEY_AD"),
("500", "TXT_KEY_AD")
)


# starting locations coordinates
tCapitals = (
(47, 41), #tBurgundy
(81, 25), #tConstantinople, Byzantium
(44, 46), #tFrance
(97, 13), #tDamascus, Arabia
(77, 30), #tPreslav, Bulgaria
(28, 28), #tCordoba
(28, 37), #tLeon, Spain
#(31, 33), #tMadrid, Spain
#(28, 32), #tToledo, Spain
(59, 57), #tNorse
(57, 34), #tVenecia
(86, 42), #tKiev
(67, 37), #tHungary
(54, 46), #tGermany
(65, 48), #tPoland
(88, 56), #tMoscow
(50, 34), #tGenoa
(43, 53), #tLondon, England
(22, 31), #tLisboa, Portugal
(63, 39), #tAustria
(79, 22), #tTurkey
(67, 64), #tSweden
(49, 52), #tDutch
(56, 27)  #Rome
) 

tStartingWorkers = (
2, #tBurgundy
0, #tByzantium
0, #tFrance
2, #tArabia
2, #tBulgaria
2, #tCordoba
3, #tSpain
2, #tNorse
3, #tVenecia
3, #tKiev
3, #tHungary
3, #tGermany
3, #tPoland
4, #tMoscow
3, #tGenoa
3, #tEngland
3, #tPortugal
4, #tAustria
4, #tTurkey
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
(), #((57, 52), (56, 52), (58, 53)), #tAmsterdam
(), 
(), #((49, 42), (49, 44)) #tLisboa
(),
(),
(),
(),
(), 
)

tNewCapitals = (  #for RiseAndFall
((47, 41),(47, 41)), #tBurgundy -- Dijon
((81, 25), (81, 25)), #tConstantinople, Byzantium
((44, 46),(44, 46)), #tFrance -- Pairs
((85, 4), (84,3),(85,3)), #Arabia --> Alexandria (best Egyption city)
((77, 30),(77, 30)), #tPreslav, Bulgaria
((18, 14),(17, 14)), #tCordoba --> Marrakesh
((28,32),(28,31),(28,33),(27,31)), #Spain --> Toledo (like Madrid)
((59, 57),(59, 57)), #tNorse
((57, 34),(57, 34)), #tVenecia
((86, 42),(86, 42)), #tKiev
((67, 37),(67, 37)), #tHungary
((61, 49),(60, 48),(61,48),(62,48)), #tGermany --> Berlin
((65, 48),(65, 48)), #tPoland
((88, 56),(88, 56)), #tMoscow
((50, 34),(50, 34)), #tGenoa
((43, 53),(43, 53)), #tLondon, England
((22, 31),(22, 31)), #tLisboa, Portugal
((63, 39),(63, 39)), #tAustria
((79, 22),(79, 22)), #tTurkey
((67, 64),(67, 64)), #tSweden
((49, 52),(49, 52)), #tDutch
((56, 27),(56, 27))  #Rome
) 

#core areas (for RiseAndFall and Victory)

# 3Miro: tCoreArea and tNormalArea are misleading, TL is not TopLeft and BR is not BottomRight (unless the grid starts from 0,0 at TL and counts down as positive y direction)
#	TL is actually BottomLeft and BR is TopRight
#	Many functions reference those and there are search algorithm that I do not whant to change, so leave this with the comment on how to be used
#	Also Broader Area

tCoreAreasTL = ( #Core Area is initial spawn location, and also important for stability
(44,33),   #Burgundy
(66,14),   #Byzantium
(42,42),   #Franks
(93,1),   #Arabs
(74,28),   #Bulgaria
(25,18),   #Cordoba
(25,34),   #Spain
(54,56),   #Norse
(56,33),   #Venice
(80,37),   #Kiev
(65,34),   #Hungary
(52,40),   #Germany
(64,44),   #Poland
(80,52),   #Moscow
(49,27),   #Genoa
(38,48),   #England
(21,29),   #Portugal
(58,37),   #Austria
(76,16),   #Turks
(60,59),   #Sweden
(47,49),   #Netherlands
(54,25)	   #Pope
) 

tCoreAreasBR = (
(48,42),   #Burgundy
(84,26),   #Byzantium
(46,47),   #Franks
(99,15),   #Arabs
(84,36),   #Bulgaria
(35,32),   #Cordoba
(33,40),   #Spain
(59,65),   #Norse
(61,36),   #Venice
(91,48),   #Kiev
(71,39),   #Hungary
(57,48),   #Germany
(75,50),   #Poland
(95,68),   #Moscow
(53,35),   #Genoa
(45,58),   #England
(24,35),   #Portugal
(64,43),   #Austria
(84,22),   #Turks
(67,71),   #Sweden
(52,57),   #Netherlands
(58,29)	   #Pope
)


tExceptions = (  #for RiseAndFall. These are (badly named) extra squares used in spawn.
(), #Burgundy 
(), #Byzantium
(), #Frankia
(), #Arabia
(), #Bulgaria
((24, 23), (24, 22), (24, 21), (24, 20), (24, 19), (23, 22), (23, 21), (23, 20)), #Cordoba
(), #Spain
(), #Norse
(), #Venecia 
(), #Kiev
(), #Hungary
(), #Germany
(), #Poland
(), #Moscow
(), #Genoa
((39, 47), (40, 47), (41, 47)), #England
((20, 29), (22, 28), (23, 28), (24, 36), (24, 37)), #Portugal
#(), #Austria
((59, 37), (60, 37), (64, 37), (59, 44), (60, 44), (62, 44), (61, 44)), #Austria
((75,23),(75,24),(75,25),(75,26),(75,27),(76,23),(76,24),(76,25),(76,26),(76,27),(77,23),(77,24),(77,25),(77,26),(77,27),(78,23),(78,24),(78,25),(78,26),(78,27)), #Turkey
(), #Sweden
(), #Dutch
()  #Pope
)

#normal areas

tNormalAreasTL = ( #These areas are typically used for resurrection. Also used in stability and (maybe) for victory conditions
(45,33),   #Burgundy
(66,14),   #Byzantium
(35,34),   #Franks
(48,1),   #Arabs
(73,28),   #Bulgaria
(16,13),   #Cordoba
(24,25),   #Spain
(53,56),   #Norse
(56,33),   #Venice
(80,36),   #Kiev
(66,34),   #Hungary
(52,44),   #Germany
(64,43),   #Poland
(80,47),   #Moscow
(49,22),   #Genoa
(35,52),   #England
(20,28),   #Portugal
(58,37),   #Austria
(76,13),   #Turks
(60,58),   #Sweden
(48,50),   #Netherlands
(54,25)	   #Pope
) 

tNormalAreasBR = (
(49,44),   #Burgundy
(76,24),   #Byzantium
(44,49),   #Franks
(98,13),   #Arabs
(80,32),   #Bulgaria
(30,24),   #Cordoba
(41,40),   #Spain
(59,71),   #Norse
(61,36),   #Venice
(97,43),   #Kiev
(78,40),   #Hungary
(63,54),   #Germany
(78,57),   #Poland
(98,71),   #Moscow
(52,35),   #Genoa
(45,67),   #England
(25,36),   #Portugal
(65,42),   #Austria
(98,27),   #Turks
(69,71),   #Sweden
(51,54),   #Netherlands
(58,29)	   #Pope
) 


tNormalAreasSubtract = (  #These are squares subtracted from normal areas
((49, 34), (49, 35),(49, 33)), #Burgundy
(), #Byzantium
((35, 34), (36, 34), (37, 34), (38, 34), (35, 35), (36, 35), (37, 35), (35, 36), (35, 37)), #Frankia
((58,12),(72,10),(73,10),(74,10),(75,10),(78,11),(79,12),(88,11),(88,12),(89,11),(89,12),(90,12),(91,13)), #Arabia
(), #Bulgaria
(), #Cordoba
((35, 40), (36, 40), (37, 40), (38, 40), (39, 40), (40, 40), (41, 39), (41, 40), (40, 39), (39, 39), (38, 39), (37, 39), (36, 39), (35, 39), (35, 38), (36, 38), (37, 38), (38, 38), (39, 38), (40, 38), (41, 38), (37, 37), (36, 37), (38, 37), (39, 37), (40, 37), (41, 37), (41, 36), (40, 36), (39, 36), (38, 36), (37, 36), (36, 36), (38, 35), (39, 35), (40, 35), (41, 35), (41, 34), (40, 34), (39, 34), (24, 36), (24, 35), (24, 34), (24, 33), (24, 32), (24, 31), (25, 36), (25, 35), (25, 34)), #Spain
(), #Norse
(), #Venecia 
(), #Kiev
(), #Hungary
(), #Germany
(), #Poland
(), #Moscow
(), #Genoa
((35, 57), (35, 58), (36, 58), (35, 59), (36, 59)), #England
((24, 28), (25, 28), (24, 29), (25, 29), (24, 30), (25, 30), (25, 31), (25, 32), (25, 33)), #Portugal
(), #Austria
(), #Turkey
(), #Sweden
(), #Dutch
()
)


# broader areas coordinates (top left and bottom right) (for RiseAndFall)
# 3Miro: see core area comment 
# Sedna17: Currently unused?
tBroaderAreasTL = (
(42, 36), #Burgundy
(68, 14), #Byzantium
(39, 41), #France
(92,  7), #Arabia
(71, 28), #Bulgaria
(24, 23), #Cordoba
(23, 31), #Spain
(52, 53), #Norse
(52, 29), #tVenecia
(81, 37), #tKiev
(64, 27), #tHungary
(49, 41), #tGermany
(64, 42), #tPoland
(83, 51), #tMoscow
(45, 29), #tGenoa
(38, 49), #tLondon, England
(17, 27), #tLisboa, Portugal
(56, 35), #tAustria
(83, 17), #tTurkey
(62, 59), #tSweden
(44, 47), #tDutch
(54, 25)  #Pope
)

tBroaderAreasBR = (
(52, 46), #Burgundy
(83, 27), #Byzantium
(49, 51), #France
(99, 15), #Arabia
(80, 31), #Bulgaria
(34, 33), #Cordoba
(33, 41), #Spain
(62, 63), #Norse
(62, 39), #tVenecia
(91, 47), #tKiev
(74, 37), #tHungary
(58, 51), #tGermany
(74, 52), #tPoland
(93, 61), #tMoscow
(55, 39), #tGenoa
(48, 59), #tLondon, England
(27, 37), #tLisboa, Portugal
(66, 45), #tAustria
(93, 27), #tTurkey
(72, 69), #tSweden
(54, 57), #tDutch
(58, 29)  #Pope
)

# visiable areas:
tVisible = (
( (35,31,52,51),(49,26,59,38), ), # Burgundy
( (64,0,99,34),(49,1,63,38),(24,17,48,36), ), # Byzantium
( (35,31,52,51),(49,26,59,38), ), # France
( (79,0,89,6),(90,0,99,22), ), # Arabia
( (69,24,81,31),(79,31,99,41), ), # Bulgaria
( (14,17,39,33),(40,0,59,20),(60,0,95,7), ), # Cordoba
( (20,23,36,41),(37,30,48,50),(49,26,59,38), ), # Spain
( (52,55,68,66), ), # Norse
( (47,14,59,38),(60,18,63,35),(64,18,68,29), ), # Venice
( (77,24,82,42),(83,31,99,46), ), # Kiev
( (58,31,82,43), ), # Hungary
( (35,33,48,51),(49,27,63,55), ), # Germany
( (57,36,76,55),(77,40,99,46), ), # Poland
( (70,33,99,58),(74,59,99,69), ), # Moscow
( (33,20,63,37),(64,9,82,28), ), # Genoa
( (30,51,46,68),(35,46,46,50), ), # England
( (18,23,36,42), ), # Portugal
( (35,33,48,51),(49,27,63,55), ), # Austria
( (77,14,99,27),(93,5,99,13), ), # Turkey
( (52,53,74,72), ), # Sweden
( (42,42,65,66), ), # Dutch
( (39,12,73,44), ), # Pope
)


# 3Miro: Initial Wars, note only the upper triangle of the array is valid, the lower should be all zeros
tWarAtSpawn = (
#Bur Byz Fra Ara Bul Cor Spa Nor Ven Kie Hun Ger Pol Mos Gen Eng Por Aus Tur Swe Dut Pop In1 In2 In3 In4
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Bur
( 0,  0,  0, 90, 90,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 90,  0,  0,  0,  0,  0,  0,  0, ), #Byz
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 60,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Fra
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 60,  0,  0,  0,  0,  0,  0,  0, ), #Ara
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Bul
( 0,  0,  0,  0,  0,  0, 80,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Cor
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Spa
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Nor
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Ven
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Kie
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Hun
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Ger
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Pol
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Mos
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Gen
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Eng
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Por
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Aus
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 50, 50, 50, 50, ), #Tur
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Swe
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Dut
)

iMercPromotion = 48

#Mercenaries. Higher number = less likely to hire
tHire = (
10, #Burgundy
10, #Byzantium
30, #Frankia
50, #Arabia
10, #Bulgaria 
50, #Cordoba
40, #Spain
10, #Norse
30, #Venecia
40, #Kiev
10, #Hungary
70, #Germany
60, #Poland
60, #Moscow
30, #Genoa
70, #England
40, #Portugal
20, #Austria
80, #Turkey
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
0, #Burgundy
1, #Byzantium
1, #Frankia
2, #Arabia
2, #Bulgaria
1, #Cordoba
2, #Spain
2, #Norse
0, #Venecia
1, #Kiev
2, #Hungary
1, #Germany
0, #Poland
1, #Moscow
0, #Genoa
1, #England
2, #Portugal
1, #Austria
2, #Turkey
2, #Sweden
0, #Dutch
0  #Pope
)


#war during rise of new civs higher number means less war
tAIStopBirthThreshold = (
    20, #Burgundy
    30, #Byzantium
    60, #Frankia
    50, #Arabia
    70, #Bulgaria
    10, #Cordoba
    80, #Spain
    70, #Norse
    30, #Venecia
    80, #Kiev
    80, #Hungary
    80, #Germany
    40, #Poland
    70, #Moscow
    40, #Genoa
    80, #England
    30, #Portugal
    30, #Austria
    80, #Turkey
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
10, #Burgundy
40, #Byzantium
80, #Frankia
60, #Arabia
30, #Bulgaria
50, #Cordoba
80, #Spain
60, #Norse
20, #Venecia
50, #Kiev
50, #Hungary
70, #Germany
60, #Poland
80, #Moscow
10, #Genoa
70, #England
60, #Portugal
70, #Austria
60, #Turkey
70, #Sweden
60, #Dutch
90  #Pope
)  

#Sedna17 Respawn: These dates are the most likely times for each civ to have its special opportunity to respawn
tRespawnTime = (
245, #Burgundy 1335 -- so they can participate in 100 years war and act as Valois Duchy of Burgundy
999, #Byzantium -- no special respawn
350, #Frankia 1600 -- France united to modern borders + start of Bourbon royal line. 
190, #Arabia 1170 -- Ayyubid dynasty from Egypt to cause problems for Crusaders 
195, #Bulgaria 1185 -- Second Bulgarian empire
174, #Cordoba 1122 -- Almohads, better timing than Almoravids
290, #Spain 1467 -- Union of Castile/Aragon and ready for colonies
265, #Norse 1395 -- Kalmar Union
999, #Venecia -- no special respawn
999, #Kiev -- no special respawn
999, #Hungary -- no special respawn
401, #Germany 1701 -- Prussia
999, #Poland -- no special respawn
999, #Moscow -- no special respawn
999, #Genoa -- no special respawn
380, #England 1660 -- Restoration of Monarchy (also leading up to Scottish Union)
267, #Portugal 1400 -- Make sure Portugal is around for colonies
313, #Austria 1526 -- Battle of Mohacs, Habsburgs take over Hungary
294, #Turkey 1482 -- End of Mehmed II conquest. 
999, #Sweden -- no special respawn
999, #Dutch -- no special respawn
999  #Pope -- no special respawn
)


#Congresses.
tPatienceThreshold = (
30, #Burgundy
30, #Byzantium
30, #Frankia
30, #Arabia
30, #Bulgaria
30, #Cordoba
30, #Spain
30, #Norse
30, #Venecia
30, #Kiev
30, #Hungary
30, #Germany
30, #Poland
30, #Moscow
30, #Genoa
30, #England
30, #Portugal
30, #Austria
30, #Turkey
30, #Sweden
30  #Dutch
) 


# religion spread modifiers:
tReligionSpreadFactor = ( # PROT, ISL, CATH, ORTH, JUD
(150,  20, 150,  70,  10), #Burgundy
(100,  50,  70, 150,  10), #Byzantium
(150,  20, 250,  70,  10), #France
( 20, 350,  50,  10,  10), #Arabia
(100,  50, 100, 350,  10), #Bulgaria
( 50, 250, 100,  20,  10), #Cordoba
(100,  20, 200,  20,  10), #Spain
(250,  50, 100, 150,  10), #Norse
( 90,  50, 200,  30,  10), #tVenecia
( 90,  90,  90, 250,  10), #tKiev
(250,  80, 150, 100,  10), #tHungary
(450,  20, 250,  20,  10), #tGermany
(200, 100, 400, 200,  10), #tPoland
(100,  20, 100, 250,  10), #tMoscow
(190,  50, 250,  30,  10), #tGenoa
(450,  20, 100,  20,  10), #tEngland
(200,  80, 250,  20,  10), #tPortugal
(200,  20, 250,  20,  10), #tAustria
( 20, 350,  80,  80,  10), #tTurkey
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


tLeaders = (		#First has to be the primary leader (the one that appaers on the civ selection screen). Can be changed in the WB file (AbsintheRed)
(xml.iCharles_V,),
(xml.iJustinian,),
(xml.iCharlemagne, xml.iJoan, xml.iLouis_Xiv),
(xml.iAbuBakr, xml.iSaladin),
(xml.iSimeon,),
(xml.iAbdarRahman, xml.iAbuYusufYaqub),
(xml.iIsabella, xml.iPhilip_Ii),
(xml.iHarald_Hardrada, xml.iHaakon_Iv, xml.iChristian_Iv),
(xml.iDandolo, xml.iAndrea_Dandolo),
(xml.iYaroslav,),
(xml.iStephen, xml.iMatthias),
(xml.iBarbarossa, xml.iFrederick),
(xml.iCasimir, xml.iSobieski),
(xml.iIvan_Iv, xml.iPeter, xml.iCatherine),		#Don't change back the order of Peter and Ivan. Right now Ivan is the primary leader. Was needed for leader switching (AbsintheRed - Beta 6)
(xml.iSimone,),
(xml.iWilliam, xml.iElizabeth,xml.iGeorge_Iii),
(xml.iAfonso, xml.iJoao, xml.iMaria_Ii),
(xml.iMaximilian, xml.iMaria_Theresa),
(xml.iMehmed, xml.iSuleiman),
(xml.iGustavus,),
(xml.iWillem_Van_Oranje,),
(xml.iThe_Pope,)
)


tEarlyLeaders = (		#Don't have to be the same as the primary leader (AbsintheRed)
(xml.iCharles_V),
(xml.iJustinian),
(xml.iCharlemagne),
(xml.iAbuBakr),
(xml.iSimeon),
(xml.iAbdarRahman),
(xml.iIsabella),
(xml.iHarald_Hardrada),
(xml.iDandolo),
(xml.iYaroslav),
(xml.iStephen),
(xml.iBarbarossa),
(xml.iCasimir),
(xml.iIvan_Iv),
(xml.iSimone),
(xml.iWilliam),
(xml.iAfonso),
(xml.iMaximilian),
(xml.iMehmed),
(xml.iGustavus),
(xml.iWillem_Van_Oranje),
(xml.iThe_Pope)
)


tLateLeaders = (		#All switch dates up to 200 years earlier because the switch is triggered after a few years (date, percentage, era)
(xml.iCharles_V,),
(xml.iJustinian,),
(xml.iJoan, xml.i1160AD, 10, 2, xml.iLouis_Xiv, xml.i1452AD, 25, 3),
(xml.iSaladin, xml.i1160AD, 25, 2),
(xml.iSimeon,),
(xml.iAbuYusufYaqub, xml.i1101AD, 10, 2),
(xml.iPhilip_Ii, xml.i1520AD, 10, 3),
(xml.iHaakon_Iv, xml.i1160AD, 25, 2, xml.iChristian_Iv, xml.i1520AD, 5, 3),
(xml.iAndrea_Dandolo, xml.i1200AD, 10, 2),
(xml.iYaroslav,),
(xml.iMatthias, xml.i1452AD, 5, 3),
(xml.iFrederick, xml.i1520AD, 5, 3),
(xml.iSobieski, xml.i1570AD, 10, 3),
(xml.iPeter, xml.i1570AD, 10, 3, xml.iCatherine, xml.i1700AD, 25, 3),
(xml.iSimone,),
(xml.iElizabeth, xml.i1452AD, 10, 3, xml.iGeorge_Iii, xml.i1700AD, 10, 3),
(xml.iJoao, xml.i1419AD, 10, 3, xml.iMaria_Ii, xml.i1700AD, 10, 3),
(xml.iMaria_Theresa, xml.i1700AD, 25, 3),
(xml.iSuleiman, xml.i1520AD, 15, 3),
(xml.iGustavus,),
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
iUP_PromotionI = 10		# give a promotion to all units
iUP_PromotionII = 11		# give a second promotion to all units
iUP_CanEnterTerrain = 12	# all unit can enter some terrain type
iUP_NoResistance = 13		# no resistance from conquering cities
iUP_Conscription = 14		# can draft from cities with foreign culture
iUP_Inquisition = 15		# no instability from religious prosecution
iUP_Emperor = 16		# no civil war and no secession in the core (Python only)
iUP_Faith = 17			# state religion spreads to newly accuired cities (found/trade/conquest) with a temple (Python only)
iUP_Mercenaries = 18		# halves the cost of mercenaries (Python only)
iUP_LandStability = 19		# no penalty from owning unstable land (Python only)
iUP_Discovery = 20		# lower cost of a block of projects
iUP_EndlessLand = 21		# lower civic cost assosiated with cities
iUP_ForeignSea = 22		# allows the ships to enter foreign sea territory (Dutch UP from RFC)
iUP_Pious = 23			# increase the gain (and loss) of Faith Points

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
