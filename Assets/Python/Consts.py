# Rhye's and Fall of Civilization - Constants


# globals

#from CvPythonExtensions import *
#gc = CyGlobalContext()

l0Array =       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 3Miro for stability, counts the cities for each player
l0ArrayActive = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
l0ArrayTotal =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # this is just a dummy array

lm1Array =      [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

# 3Miro: map size entered here
iMapMaxX = 100
iMapMaxY = 73

# initialise player variables to player IDs from WBS
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
tAmericasTL = (3, 0)
tAmericasBR = (43, 63)


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
[], #Burgundy
[], #Byzantium
[], #Frankia
[iByzantium], #Arabia
[iByzantium], #Bulgaria
[], #Cordoba
[iCordoba], #Spain
[], #Norse
[iPope], #Venecia
[iBulgaria], #Kiev
[iBulgaria], #Hungary
[iHungary,iVenecia], #Germany
[iGermany,iKiev], #Poland
[iKiev,iPoland], #Moscow
[iVenecia,iGermany,iHungary,iPope], #Genoa
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
0,  #500AD Burgundy
0,  #500AD Byzantium
0,  #500AD Frankia
33, #632AD Arabia
45, #680AD Bulgaria
53, #712AD Cordoba
104, #720AD Spain => 1083 (161) => 909
68, #770AD Norse
75, #800AD Venecia
95, #880AD Kiev
100,#900AD Hungary
113,#940AD Germany
123,#970AD Poland
241,#1000AD Moscow => 1323
140,#1020AD Genoa
153,#1060AD England
167,#1100AD Portugal
187,#1160AD Austria
233,#1300AD Turkey
300,#1500AD Sweden
340,#1580AD Dutch
0,	#Pope
0,
0,
0,
0,
0
) # 3Miro: tBirth should finish with zeros for all minor civs (indeps, barbs and celts in original RFC)


tYear = (
("500", "TXT_KEY_AD"),
("500", "TXT_KEY_AD"),
("500", "TXT_KEY_AD"),
("632", "TXT_KEY_AD"),
("640", "TXT_KEY_AD"),
("700", "TXT_KEY_AD"),
("909", "TXT_KEY_AD"),
("770", "TXT_KEY_AD"),
("800", "TXT_KEY_AD"),
("880", "TXT_KEY_AD"),
("900", "TXT_KEY_AD"),
("940", "TXT_KEY_AD"),
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

# 3Miro: wrong order. Use order as in the WB
tGoals = (
("TXT_KEY_UHV_BUR1", "TXT_KEY_UHV_BUR2", "TXT_KEY_UHV_BUR3"),
("TXT_KEY_UHV_BYZ1", "TXT_KEY_UHV_BYZ2", "TXT_KEY_UHV_BYZ3"),
("TXT_KEY_UHV_FRA1", "TXT_KEY_UHV_FRA2", "TXT_KEY_UHV_FRA3"),
("TXT_KEY_UHV_ARA1", "TXT_KEY_UHV_ARA2", "TXT_KEY_UHV_ARA3"),
("TXT_KEY_UHV_BUL1", "TXT_KEY_UHV_BUL2", "TXT_KEY_UHV_BUL3"),
("TXT_KEY_UHV_COR1", "TXT_KEY_UHV_COR2", "TXT_KEY_UHV_COR3"),
("TXT_KEY_UHV_SPN1", "TXT_KEY_UHV_SPN2", "TXT_KEY_UHV_SPN3"),
("TXT_KEY_UHV_NOR1", "TXT_KEY_UHV_NOR2", "TXT_KEY_UHV_NOR3"),
("TXT_KEY_UHV_VEN1", "TXT_KEY_UHV_VEN2", "TXT_KEY_UHV_VEN3"),
("TXT_KEY_UHV_KIE1", "TXT_KEY_UHV_KIE2", "TXT_KEY_UHV_KIE3"),
("TXT_KEY_UHV_HUN1", "TXT_KEY_UHV_HUN2", "TXT_KEY_UHV_HUN3"),
("TXT_KEY_UHV_GER1", "TXT_KEY_UHV_GER2", "TXT_KEY_UHV_GER3"),
("TXT_KEY_UHV_POL1", "TXT_KEY_UHV_POL2", "TXT_KEY_UHV_POL3"),
("TXT_KEY_UHV_MOS1", "TXT_KEY_UHV_MOS2", "TXT_KEY_UHV_MOS3"),
("TXT_KEY_UHV_GEN1", "TXT_KEY_UHV_GEN2", "TXT_KEY_UHV_GEN3"),
("TXT_KEY_UHV_ENG1", "TXT_KEY_UHV_ENG2", "TXT_KEY_UHV_ENG3"),
("TXT_KEY_UHV_POR1", "TXT_KEY_UHV_POR2", "TXT_KEY_UHV_POR3"),
("TXT_KEY_UHV_AUS1", "TXT_KEY_UHV_AUS2", "TXT_KEY_UHV_AUS3"),
("TXT_KEY_UHV_TUR1", "TXT_KEY_UHV_TUR2", "TXT_KEY_UHV_TUR3"),
("TXT_KEY_UHV_SWE1", "TXT_KEY_UHV_SWE2", "TXT_KEY_UHV_SWE3"),
("TXT_KEY_UHV_DUT1", "TXT_KEY_UHV_DUT2", "TXT_KEY_UHV_DUT3"),
("TXT_KEY_UHV_POP1", "TXT_KEY_UHV_POP2", "TXT_KEY_UHV_POP3")
)


# date waypoints
# 3Miro: important years
i500AD = 0
i632AD = 33
i640AD = 35
i700AD = 50
i712AD = 53
i720AD = 55
i770AD = 68
i800AD = 75
i840AD = 85
i880AD = 95
i900AD = 100
i940AD = 113
i960AD = 120
i970AD = 123
i1000AD =133
i1020AD =140
i1050AD =150
i1053AD =151
i1060AD =153
i1080AD =160
i1101AD =167
i1160AD =187
i1200AD =200
i1236AD =212
i1248AD =216
i1281AD =227
i1284AD =228
i1300AD =233
i1320AD =240
i1350AD =250
i1359AD =253
i1401AD =267
i1419AD =273
i1431AD =277
i1449AD =283
i1452AD =284
i1461AD =287
i1470AD =290
i1482AD =294
i1491AD =297
i1500AD =300
i1520AD =310
i1526AD =313
i1540AD =320
i1570AD =335
i1580AD =340
i1600AD =350
i1620AD =360
i1640AD =370
i1650AD =375
i1660AD =380
i1670AD =385
i1680AD =390
i1700AD =400
i1730AD =430
i1750AD =450





# starting locations coordinates
tCapitals = (
(47, 41), #tBurgundy
(81, 25), #tConstantinople, Byzantium
(44, 46), #tFrance
(97, 13), #tDamascus, Arabia
(77, 30), #tPresalv, Bulgaria
(28, 28), #tCordoba
(28, 37), #tLeon, Spain
#(31, 33), #tMadrid, Spain
#(28, 32), #tToledo, Spain
(59, 57), #tNorse
(57, 34), #tVenecia
(86, 42), #tKiev
(67, 37), #tHungary
(54, 46), #tGermany
(69, 47), #tPoland
(88, 56), #tMoscow
(50, 34), #tGenoa
(43, 53), #tLondon, England
(22, 31), #tLisboa, Portugal
(63, 39), #tAustria
(88, 22), #tTurkey
(67, 64), #tSweden
(49, 52), #tDutch
(56, 27)  #Rome
) 

tStartingWorkers = (
0, #tBurgundy
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

#core areas (for RiseAndFall and Victory)

# 3Miro: tCoreArea and tNormalArea are misleading, TL is not TopLeft and BR is not BottomRight (unless the grid starts from 0,0 at TL and counts down as positive y direction)
#	TL is actually BottomLeft and BR is TopRight
#	Many functions reference those and there are search algorithm that I do not whant to change, so leave this with the comment on how to be used
#	Also Broader Area

tCoreAreasTL = (
(47,37),   #Burgundy
(71,14),   #Byzantium
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
(50,27),   #Genoa
(38,48),   #England
(21,30),   #Portugal
(58,37),   #Austria
(85,18),   #Turks
(60,59),   #Sweden
(48,49),   #Netherlands
(54,25)	   #Pope
) 

tCoreAreasBR = (
(51,48),   #Burgundy
(84,26),   #Byzantium
(46,47),   #Franks
(99,15),   #Arabs
(84,36),   #Bulgaria
(35,32),   #Cordoba
(33,40),   #Spain
(59,65),   #Norse
(61,36),   #Venice
(91,48),   #Kiev
(72,42),   #Hungary
(57,48),   #Germany
(75,50),   #Poland
(95,68),   #Moscow
(53,35),   #Genoa
(45,58),   #England
(24,35),   #Portugal
(64,43),   #Austria
(99,27),   #Turks
(67,71),   #Sweden
(53,54),   #Netherlands
(58,29)	   #Pope
)


tExceptions = (  #for RiseAndFall
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
((20, 29), (22, 28), (23, 28), (24, 28), (24, 36), (24, 37)), #Portugal
#(), #Austria
((59, 37), (60, 37), (64, 37), (59, 44), (60, 44), (62, 44), (61, 44)), #Austria
(), #Turkey
(), #Sweden
(), #Dutch
()  #Pope
)



#normal areas (for Victory and resurrection)

tNormalAreasTL = (
(45,33),   #Burgundy
(66,14),   #Byzantium
(35,34),   #Franks
(48,1),   #Arabs
(73,28),   #Bulgaria
(16,17),   #Cordoba
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
(77,14),   #Turks
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


tNormalAreasSubtract = (  #for resurrection and stability
((49, 34), (49, 35),(49, 33)), #Burgundy
(), #Byzantium
((35, 34), (36, 34), (37, 34), (38, 34), (35, 35), (36, 35), (37, 35), (35, 36), (35, 37)), #Frankia
(), #Arabia
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
( (79,14,99,27),(93,5,99,13), ), # Turkey
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
10, #Byzantium
90, #Frankia
30, #Arabia
30, #Bulgaria
20, #Cordoba
90, #Spain
80, #Norse
40, #Venecia
60, #Kiev
70, #Hungary
80, #Germany
60, #Poland
80, #Moscow
10, #Genoa
70, #England
70, #Portugal
80, #Austria
50, #Turkey
70, #Sweden
60, #Dutch
90  #Pope
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




# initialise religion variables to religion indices from XML
iProtestantism = 0
iIslam = 1
iCatholicism = 2
iOrthodoxy = 3
iJudaism = 4
iNumReligions = 5

# religion spread modifiers:
tReligionSpreadFactor = ( # PROT, ISL, CATH, ORTH, JUD
(350,  20, 350,  70,  10), #Burgundy
(100,  50,  70, 350,  10), #Byzantium
(200,  20, 350,  70,  10), #France
( 20, 350,  50,  10,  10), #Arabia
(100,  50, 250, 350,  10), #Bulgaria
( 50, 350, 100,  20,  10), #Cordoba
(180,  20, 350,  20,  10), #Spain
(250,  50, 100, 150,  10), #Norse
( 90,  50, 350,  30,  10), #tVenecia
( 90,  90,  90, 350,  10), #tKiev
(250,  80, 250, 150,  10), #tHungary
(450,  20, 350,  20,  10), #tGermany
(200,  20, 350,  80,  10), #tPoland
(100,  20, 100, 250,  10), #tMoscow
(190,  50, 350,  30,  10), #tGenoa
(450,  20, 100,  20,  10), #tEngland
(190,  80, 350,  20,  10), #tPortugal
(200,  20, 350,  20,  10), #tAustria
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

### Reformation Begin ###       
#Matrix determines how likely the AI is to switch to Protestantism                                                               
lReformationMatrix = [
50, #Burgundy
10, #Byzantium
40, #France
10, #Arabia
30, #Bulgaria
10, #Cordoba
10, #Spain
80, #Norse
30, #Venecia
20, #Kiev
50, #Hungary
90, #Germany
30, #Poland
10, #Moscow
30, #Genoa
80, #England
30, #Portugal
50, #Austria
10, #Turkey
90, #Sweden
90, #Dutch
0,  #Rome
0,  #Indies and Barbs
0,
0,
0,
0
] 
### Reformation End ###    


# initialise tech variables to unit indices from XML

#Early
iCalendar=0
iArchitecture=1
iBronzeCasting=2
iTheology=3
iManorialism=4
iStirrup=5
iEngineering=6
iChainMail=7
iArt=8
iMonasticism=9
iVassalage=10
iAstrolabe=11
iMachinery=12
iVaultedArches=13
iMusic=14
iHerbalMedicine=15
iFeudalism=16
iFarriers=17
#High
iMapMaking=18
iBlastFurnace=19
iSiegeEngines=20
iGothicArchitecture=21
iLiterature=22
iCodeOfLaws=23
iAristocracy=24
iLateenSails=25
iPlateArmor=26
iMonumentBuilding=27
iClassicalKnowledge=28
iAlchemy=29
iCivilService=30
iClockmaking=31
iPhilosophy=32
iEducation=33
iGuilds=34
iChivalry=35
#Late
iOptics=36
iReplaceableParts=37
iPatronage=38
iGunpowder=39
iBanking=40
iMilitaryTradition=41
iShipbuilding=42
iDrama=43
iDivineRight=44
iChemistry=45
iPaper=46
iProfessionalArmy=47
iPrintingPress=48
iPublicWorks=49
iMatchlock=50
iArabicKnowledge=51
#Renaissance
iAstronomy=52
iSteamEngines=53
iConstitution=54
iPolygonalFort=55
iArabicMedicine=56
iRenaissanceArt=57
iNationalism=58
iLiberalism=59
iScientificMethod=60
iMilitaryTactics=61
iNavalArchitecture=62
iCivilEngineering=63
iRightOfMan=64
iEconomics=65
iPhysics=66
iBiology=67
iCombinedArms=68
iTradingCompanies=69
iMachineTools=70
iFreeMarket=71
iExplosives=72
iMedicine=73
iIndustrialTech=74

iNumTechs = 75
iFutureTech = 74

iNumTechsFuture = 1


# initialise unit variables to unit indices from XML

iLion= 0
iBear= 1
iPanther= 2
iWolf= 3
iSettler= 4
iWorker= 5
iExecutive1= 6
iExecutive2= 7
iExecutive3= 8
iExecutive4= 9
iExecutive5= 10
iExecutive6= 11
iExecutive7= 12
iCatholicMissionary= 13
iOrthodoxMissionary= 14
iProtestantMissionary= 15
iIslamicMissionary= 16
iArcher= 17
iCrossbowman= 18
iArbalest= 19
iGenoaBalestrieri= 20
iLongbowman= 21
iEnglishLongbowman= 22
iSpearman= 23
iGuisarme= 24
iPikeman= 25
iHolyRomanLandsknecht= 26
iAxeman= 27
iVikingBeserker= 28
iSwordsman= 29
iLongSwordsman= 30
iKnightofStJohns= 31
iMaceman= 32
iPortugalFootKnight= 33
iGrenadier= 34
iNetherlandsGrenadier= 35
iArquebusier= 36
iMusketman= 37
iSwedishKarolin= 38
iSpanishTercio= 39
iFrenchMusketeer= 40
iLineInfantry= 41
iDragoon= 42
iScout= 43
iBulgarianKonnik= 44
iHorseArcher= 45
iHungarianLancer= 46
iMountedInfantry= 47
iPistolier= 48
iHussar= 49
iLancer= 50
iCordobanBerber= 51
iHeavyLancer= 52
iArabiaGhazi= 53
iByzantineCataphract= 54
iKnight= 55
iTemplar= 56
iTeutonic= 57
iMoscowBoyar= 58
iPolishWingedHussar= 59
iBurgundianPaladin= 60
iCuirassier= 61
iAustrianKurassier= 62
iKievDruzhina= 63
iCatapult= 64
iTrebuchet= 65
iBombard= 66
iTurkeyGreatBombard= 67
iCannon= 68
iFieldArtillery= 69
iWorkboat= 70
iGalley= 71
iWarGalley= 72
iCaravel= 73
iCogge= 74
iVeniceGalleas= 75
iCarrack= 76
iGalleon= 77
iHolk= 78
iPrivateer= 79
iFrigate= 80
iSpy= 81
iProsecutor= 82
iProphet= 83
iArtist= 84
iScientist= 85
iMerchant= 86
iEngineer= 87
iGreatGeneral= 88
iGreatSpy= 89
iMongolKeshik= 90
iHighlander= 91
iWelshLongbowman= 92
iTagmata= 93
iSeljuk= 94
iGunGalley=95

iProsecutorClass = 64



# initialise bonuses variables to bonuses IDs from WBSinulAi
iRelic = 0 #This is actually the relic bonus, sorry
iCoal = 1
iCopper = 2
iHorse = 3
iIron = 4
iMarble = 5
iOil = 6
iStone = 7
iUranium = 8
iBanana = 9
iClam = 10
iCorn = 11
iCow = 12
iCrab = 13
iDeer = 14
iFish = 15
iPig = 16
iRice = 17
iSheep = 18
iWheat = 19
iDye = 20
iFur = 21
iGems = 22
iGold = 23
iIncense = 24
iIvory = 25
iSilk = 26
iSilver = 27
iSpices = 28
iSugar = 29
iWine = 30
iWhale = 31
iDrama = 32
iMusicals = 33
iMovies = 34
iCotton = 35
iApple = 36
iBarley = 37
iHoney = 38
iPotato = 39
iSalt = 40
iSulphur = 41
iTimber = 42
iCoffee = 43
iSlaves = 44
iTea = 45
iTobacco = 46
iOlives = 47
iAccess = 48
iNorthAccess = 49
iSouthAccess = 50
iAsiaAccess = 51

#Buildings

iPalace = 0
iGreatPalace = 1
iSummerPalace = 1 #
iRoyalAcademy = 2
iVersailles = 3
iForbiddenPalace = 3 #
iWalls = 4
iCelticDun = 5
iCastle = 6
iMoscowKremlin = 7
iHungarianStronghold = 8
iSpanishCitadel = 9
iBarracks = 10
iSwedishTennant = 11
iArcheryRange = 12
iSiegeWorkshop = 13
iStable = 14
iBulgarianStan = 15
iGranary = 16
iCordobanNoria = 17
iPolishFolwark = 18
iAqueduct = 19
iOttomanHammam = 20
iLighthouse = 21
iVikingTradingPost = 22
iWharf = 23
iHarbor = 24
iCustomHouse = 25
iPortugalFeitoria = 26
iDrydock = 27
iVeniceArsenal = 28
iForge = 29
iCarpenter = 30
iMason = 31
iGuildHall = 32
iTextileMill = 33
iObelisk = 34
iTowerLondon = 35
iUniversity = 36
iObservatory = 37
iFrenchSalon = 38
iHospital = 39
iTheatre = 40
iByzantineHippodrome = 41
iAustrianOperaHouse = 42
iMarket = 43
iBrewery = 44
iJeweler = 45
iWeaver = 46
iSmokehouse = 47
iTanner = 48
iButcher = 49
iGrocer = 50
iLuxuryStore = 51
iWarehouse = 52
iApothecary = 53
iBank = 54
iGenoaMint = 55
iEnglishStockExchange = 56
iCourthouse = 57
iKievVeche = 58
iHolyRomanRathaus = 59
iTollHouse = 60
iDungeon = 61
iNightWatch = 62
iLevee = 63
iNetherlandsDike = 64
iInn = 65
iCoffeeHouse = 66
iManorHouse = 67
iBurgundianChateau = 68
iHerbalist = 69
iInfirmary = 70
iPaganShrine = 71
iJewishQuarter = 72
iProtestantTemple = 73
iProtestantSchool = 74
iProtestantCathedral = 75
iProtestantChapel = 76
iProtestantSeminary = 77
iProtestantShrine = 78
iIslamicTemple = 79
iIslamicChapel = 80
iIslamicCathedral = 81
iIslamicReliquary = 82
iIslamicSchool = 83
iIslamicMadrassa = 84
iIslamicShrine = 85
iCatholicTemple = 86
iCatholicCathedral = 87
iCatholicChapel = 88
iCatholicReliquary = 89
iCatholicSchool = 90
iCatholicMonastery = 91
iCatholicScriptorium = 92
iCatholicSeminary = 93
iCatholicShrine = 94
iOrthodoxTemple = 95
iOrthodoxCathedral = 96
iOrthodoxChapel = 97
iOrthodoxReliquary = 98
iOrthodoxSchool = 99
iOrthodoxMonastery = 100
iOrthodoxScriptorium = 101
iOrthodoxSeminary = 102
iOrthodoxShrine = 103
iSistineChapel = 104
iNotreDame = 105
iLeaningTower = 106
iTheodosianWalls = 107
iTopkapiPalace = 108
iShrineofUppsala = 109
iNationalTheatre = 110
iHermitage = 111
iOxfordUniversity = 112
iHeroicEpic = 113
iAlhambra = 114
iKrakDesChevaliers = 115
iSanMarco = 116
iLaMezquita = 117
iStBasil = 118
iMagnaCarta = 119
iSophiaKiev = 120
iDomeRock = 121
iBrandenburg = 122
iRibeira = 123
iMonasteryofCluny = 124
iRoundChurch = 125
iCorporation1 = 126
iCorporation2 = 127
iCorporation3 = 128
iCorporation4 = 129
iCorporation5 = 130
iCorporation6 = 131
iCorporation7 = 132
iCaravanHouse = 133
iLeonardo = 134
iGardens = 135
iMagellan = 136
iMarcoPolo = 137
iEscorial = 138
iTempleMount = 139
iBelemTower = 140
iGoldenBull = 141
iKalmar = 142
iPalaisPapes = 143
iTombAlKhalid = 144
iStephansdom = 145
iBibliotheca = 146
iFontainebleau = 147
iImperialDiet = 148
iAmdamBeurs = 149
iCopernicus = 150
iSanGiorgio = 151
iWestminster = 152
iPressburg = 153
iNationalEpic = 154
iTriumphalArch = 154 #Should be same number as National Epic
iNumBuildings = 155 #Should equal iPlague
iPlague = 155
iNumBuildingsPlague = 156
iNumCorporations = 7 # to mark Genoa's UHV as false

#Projects

iEastIndiaCompany = 0
iWestIndiaCompany = 1
iEncyclopedie = 2
iNumNotColonies = 3
iNumTotalColonies = 15

#Eras

iAncient = 0
iClassical = 1
iMedieval = 2
iRenaissance = 3
iIndustrial = 4
iModern = 5
iFuture = 6


#Improvements

iRoad = 0

#feature & terrain

iIce = 0
iJungle = 1
iDenseForest = 2
iOasis = 3
iFloodPlains = 4
iForest = 5
iFallout = 6
iMud = 7

iDesert = 2
iTundra = 3
iMarsh = 9



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



#leaders
iLeaderBarbarian = 0
iAlexander = 1
iAsoka = 2
iAugustus = 3
iBismarck = 4
iBoudica = 5
iBrennus = 6
iCatherine = 7
iCharlemagne = 8
iOttoI = 8
iChurchill = 9
iCyrus = 10
iDarius = 11
iDe_Gaulle = 12
iElizabeth = 13
iFrederick = 14
iGandhi = 15
iGenghis_Khan = 16
iGilgamesh = 17
iHammurabi = 18
iHannibal = 19
iHatshepsut = 20
iHuayna_Capac = 21
iIsabella = 22
iJoao = 23
iJulius_Caesar = 24
iJustinian = 25
iKublai_Khan = 26
iLincoln = 27
iLouis_Xiv = 28
iMansa_Musa = 29
iMao = 30
iMehmed = 31
iMontezuma = 32
iNapoleon = 33
iPacal = 34
iPericles = 35
iPeter = 36
iQin_Shi_Huang = 37
iRamesses = 38
iRagnar = 39
iFranklin_Roosevelt = 40
iSaladin = 41
iShaka = 42
iSitting_Bull = 43
iStalin = 44
iSuleiman = 45
iSuryavarman = 46
iTokugawa = 47
iVictoria = 48
iWangkon = 49
iMing_Tai_Zu = 49
iWashington = 50
iWillem_Van_Oranje = 51
iZara_Yaqob = 52

iSalahAlDin = 43
iLeopold = 44
iSimeon = 45
iRichard = 46
iJustinian = 47
iAbdarRahman = 48
iWilliamVanOranje = 49
iElizabeth = 50
iLouisXIV = 51
iSimone = 52
iFrederick = 53
iStephen = 54
iYaroslav = 55
iPeter = 56
iRagnar = 57
iCasimir = 58
iJoao = 59
iIsabella = 60
iGustavus = 61
iSuleiman = 62
iDandolo = 63
iPietro = 64
iThePope = 65


# 3Miro - for late Roman Justinian in, should not be used in RFCE
#if (gc.getPlayer(0).isPlayable()): #late start condition
#        tRomanLateLeaders = (iAugustus, i50AD, 5, 2, iJustinian, i1000AD, 10, 3)
#else: 
#        tRomanLateLeaders = (iAugustus, i50AD, 5, 2)

tLeaders = (
(iRichard,),
(iJustinian,),
(iLouis_Xiv,),
(iSalahAlDin,),
(iSimeon,),
(iAbdarRahman,),
(iIsabella,),
(iRagnar,),
(iDandolo,),
(iYaroslav,),
(iStephen,),
(iFrederick,),
(iCasimir,),
(iPeter,),
(iSimone,),
(iElizabeth,),
(iJoao,),
(iLeopold,),
(iSuleiman,),
(iGustavus,),
(iWilliamVanOranje,),
(iThePope,)
)

tEarlyLeaders = (
(iRichard),
(iJustinian),
(iLouis_Xiv),
(iSalahAlDin),
(iSimeon),
(iAbdarRahman),
(iIsabella),
(iRagnar),
(iDandolo),
(iYaroslav),
(iStephen),
(iFrederick),
(iCasimir),
(iPeter),
(iSimone),
(iElizabeth),
(iJoao),
(iLeopold),
(iSuleiman),
(iGustavus),
(iWilliamVanOranje),
(iThePope)
)


tLateLeaders = ( #all up to 300 turns earlier because the switch is triggered after a few years
(iRichard,),
(iJustinian,),
(iLouis_Xiv,),
(iSalahAlDin,),
(iSimeon,),
(iAbdarRahman,),
(iIsabella,),
(iRagnar,),
(iDandolo,),
(iYaroslav,),
(iStephen,),
(iFrederick,),
(iCasimir,),
(iPeter,),
(iSimone,),
(iElizabeth,),
(iJoao,),
(iLeopold,),
(iSuleiman,),
(iGustavus,),
(iWilliamVanOranje,),
(iThePope)
)

iImprovementWorkshop = 8
iImprovementCottage = 19
iImprovementHamlet = 20
iImprovementVillage = 21
iImprovementTown = 22

iPromotionFormation = 7
iPromotionMedicI = 13

iTerrainOcean = 8

iCivicRepublic = 4
iCivicMerchantRepublic = 19

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

iFP_Stability = 0		# stability bonus
iFP_Civic = 1			# lower civic upkeep
iFP_Growth = 2			# faster population growth
iFP_Units = 3			# lower production cost for units
iFP_Science = 4			# lower beaker cost for new techs
iFP_Production = 5		# lower cost for Wonders and Projects
iFP_Displomacy = 6		# diplomacy boost

# Saint section
iSaintBenefit = 5		# number of Faith points generated by a saint

# Crusade section
iNumCrusades = 5
iJerusalem = ( 94, 6 )

