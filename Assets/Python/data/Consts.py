# Rhye's and Fall of Civilization: Europe - Constants

from CvPythonExtensions import *
import XMLConsts as xml

# globals
gc = CyGlobalContext()

# initialize player variables to player IDs from WBS (this is the only part of the XML that will stay here):
iNumPlayers = 29
(iByzantium, iFrankia, iArabia, iBulgaria, iCordoba, iVenecia, iBurgundy, iGermany, iNovgorod, iNorway,
iKiev, iHungary, iSpain, iDenmark, iScotland, iPoland, iGenoa, iMorocco, iEngland, iPortugal,
iAragon, iSweden, iPrussia, iLithuania, iAustria, iTurkey, iMoscow, iDutch, iPope) = range(iNumPlayers)

iNumMajorPlayers = iNumPlayers

iIndependent = iNumPlayers
iIndependent2 = iNumPlayers+1
iIndependent3 = iNumPlayers+2
iIndependent4 = iNumPlayers+3
iNumTotalPlayers = iNumPlayers+4
iBarbarian = iNumPlayers+4
iNumTotalPlayersB = iBarbarian+1

(pByzantium, pFrankia, pArabia, pBulgaria, pCordoba, pVenecia, pBurgundy, pGermany, pNovgorod, pNorway,
pKiev, pHungary, pSpain, pDenmark, pScotland, pPoland, pGenoa, pMorocco, pEngland, pPortugal,
pAragon, pSweden, pPrussia, pLithuania, pAustria, pTurkey, pMoscow, pDutch, pPope) = [gc.getPlayer(i) for i in range(iNumPlayers)]

(teamByzantium, teamFrankia, teamArabia, teamBulgaria, teamCordoba, teamVenecia, teamBurgundy, teamGermany, teamNovgorod, teamNorway,
teamKiev, teamHungary, teamSpain, teamDenmark, teamScotland, teamPoland, teamGenoa, teamMorocco, teamEngland, teamPortugal,
teamAragon, teamSweden, teamPrussia, teamLithuania, teamAustria, teamTurkey, teamMoscow, teamDutch, teamPope) = [gc.getTeam(i) for i in range(iNumPlayers)]

iIndepStart = iIndependent # creates the block of independent civs
iIndepEnd = iIndependent4

#CoreAreas: Core Area is initial spawn location, no longer relevant for stability.
tCoreAreasTL = (
(66,14),   #Byzantium
(42,43),   #Franks
(92, 0),   #Arabs
(74,27),   #Bulgaria
(24,19),   #Cordoba
(55,33),   #Venice
(44,32),   #Burgundy
(51,40),   #Germany
(79,59),   #Novgorod
(53,63),   #Norway
(79,42),   #Kiev
(64,33),   #Hungary
(25,30),   #Spain
(54,55),   #Denmark
(35,62),   #Scotland
(64,43),   #Poland
(49,27),   #Genoa
(18, 3),   #Morocco
(37,48),   #England
(21,24),   #Portugal
(35,26),   #Aragon
(61,60),   #Sweden
(70,52),   #Prussia
(72,51),   #Lithuania
(59,37),   #Austria
(76,16),   #Ottomans
(84,53),   #Moscow
(46,50),   #Netherlands
(54,25)    #Pope
)

tCoreAreasBR = (
(84,26),   #Byzantium
(46,48),   #Franks
(99,12),   #Arabs
(80,30),   #Bulgaria
(37,28),   #Cordoba
(59,36),   #Venice
(48,42),   #Burgundy
(58,50),   #Germany
(82,69),   #Novgorod
(59,72),   #Norway
(88,50),   #Kiev
(73,39),   #Hungary
(32,36),   #Spain
(64,61),   #Denmark
(39,68),   #Scotland
(70,50),   #Poland
(52,35),   #Genoa
(31,16),   #Morocco
(43,60),   #England
(24,32),   #Portugal
(42,31),   #Aragon
(65,70),   #Sweden
(71,58),   #Prussia
(80,56),   #Lithuania
(62,44),   #Austria
(84,22),   #Ottomans
(97,59),   #Moscow
(52,55),   #Netherlands
(58,29)    #Pope
)

lExtraPlots = [
[], #Byzantium
[], #Frankia
[], #Arabia
[], #Bulgaria
[(26,15),(26,16),(26,17),(26,18),(27,15),(27,16),(27,17),(27,18),(28,15),(28,16),(28,17),(28,18),(29,15),(29,16),(29,17),(29,18)], #Cordoba
[(60,33),(60,34),(60,35)], #Venice
[(49,39),(49,40),(49,41),(49,42)], #Burgundy
[], #Germany
[(78,59), (78,60)], #Novgorod
[], #Norway
[], #Kiev
[], #Hungary
[], #Spain
[], #Denmark
[(37,69),(38,69)], #Scotland
[(63,46),(63,47),(63,48),(63,49),(63,50)], #Poland
[], #Genoa
[], #Morocco
[(37,46),(37,47),(38,46),(38,47),(39,46),(39,47),(40,46),(40,47),(41,46),(41,47),(42,47)], #England		3Miro: Calais shouldn't flip to them on spawn
[(25,27),(25,28),(25,29),(25,30),(25,31)], #Portugal
[(40,23),(42,23),(42,24),(44,24)], #Aragon
[(60,61),(60,62),(60,63),(61,71),(62,71),(62,72),(63,71),(63,72),(64,71),(64,72),(65,71),(65,72),(66,64),(66,65),(66,66),(66,72),(68,65),(70,67),(70,68),(71,66),(71,67),(71,68),(72,65),(72,66),(72,67)], #Sweden
[(68,51),(68,52),(68,53),(69,51),(69,52),(69,53),(70,51),(71,59),(72,57),(72,58),(73,57),(73,58),(74,57),(74,58),(74,59),(74,60),(75,57),(75,58),(75,59),(75,60),(76,58),(76,59),(76,60)], #Prussia
[(76,57),(77,57),(78,57),(79,57),(80,57)], #Lithuania
[(60,36),(61,36)], #Austria
[(76,23),(77,23),(78,23),(79,23)], #Ottomans
[(83,53),(83,54),(83,55),(83,56),(83,57),(87,60),(88,60),(89,60),(90,60),(91,60),(92,60),(93,60),(94,60),(95,60),(96,60),(97,60),(88,61),(89,61),(90,61),(91,61),(92,61),(93,61),(94,61),(95,61),(96,61),(97,61),(88,62),(89,62),(90,62),(91,62),(92,62),(93,62),(94,62),(95,62),(96,62),(97,62),(88,63),(89,63),(90,63),(91,63),(92,63),(93,63),(94,63),(95,63),(96,63),(97,63)], #Moscow
[(46,49),(47,49),(48,49),(49,49),(50,49)], #Dutch
[]  #Pope
]

#NormalAreas: Normal Area is typically used for resurrection.
tNormalAreasTL = (
(66,13),   #Byzantium
(33,32),   #Franks
(53, 0),   #Arabs
(72,27),   #Bulgaria
(43, 8),   #Cordoba
(54,32),   #Venice
(45,32),   #Burgundy
(51,43),   #Germany
(77,59),   #Novgorod
(53,63),   #Norway
(78,41),   #Kiev
(63,32),   #Hungary
(25,26),   #Spain
(54,55),   #Denmark
(34,63),   #Scotland
(63,43),   #Poland
(49,22),   #Genoa
(18, 3),   #Morocco
(32,50),   #England
(21,21),   #Portugal
(54,16),   #Aragon
(60,59),   #Sweden
(59,48),   #Prussia
(70,51),   #Lithuania
(57,36),   #Austria
(76,14),   #Turks
(83,51),   #Moscow
(47,50),   #Netherlands
(54,25)    #Pope
)

tNormalAreasBR = (
(75,24),   #Byzantium
(44,46),   #Franks
(99,11),   #Arabs
(80,31),   #Bulgaria
(52,19),   #Cordoba
(60,37),   #Venice
(49,43),   #Burgundy
(61,54),   #Germany
(88,72),   #Novgorod
(58,72),   #Norway
(91,50),   #Kiev
(77,41),   #Hungary
(34,36),   #Spain
(59,61),   #Denmark
(39,69),   #Scotland
(77,50),   #Poland
(52,36),   #Genoa
(27,13),   #Morocco
(43,62),   #England
(25,32),   #Portugal
(64,26),   #Aragon
(75,72),   #Sweden
(71,55),   #Prussia
(77,63),   #Lithuania
(63,42),   #Austria
(98,27),   #Turks
(98,63),   #Moscow
(52,54),   #Netherlands
(58,29)    #Pope
)

tNormalAreasSubtract = ( #These plots are subtracted from the tNormalAreasTL+tNormalAreasBR rectangles.
(), #Byzantium
((33,32),(33,33),(33,34),(33,35),(33,36),(34,32),(34,33),(34,34),(34,35),(35,32),(35,33),(35,34),(36,32),(36,33),(37,32),(38,32)), #Frankia
((73,10),(74,10),(75,10),(76,10),(87,10),(87,11),(88,10),(88,11),(89,11)), #Arabia
(), #Bulgaria
(), #Cordoba
((54,32),(54,33),(54,34),(55,32),(55,33),(55,34),(56,32),(56,33),(56,34),(57,32),(57,33),(58,32),(59,37),(60,36),(60,37)), #Venice
((49,32),(49,33),(49,34),(49,35),(49,36)), #Burgundy
((52,51),(52,52),(52,53),(52,54),(51,51),(51,52),(51,53),(51,54),(59,48),(59,49),(59,50),(59,51),(59,52),(59,53),(59,54),(60,48),(60,49),(60,50),(60,51),(60,52),(60,53),(60,54),(61,48),(61,49),(61,50),(61,51),(61,52),(61,53),(61,54)), #Germany
((84,59),(84,60),(85,59),(85,60),(85,61),(86,59),(86,60),(86,61),(86,62),(87,59),(87,60),(87,61),(87,62),(88,59),(88,60),(88,61),(88,62)), #Novgorod
(), #Norway
((87,41),(88,41),(89,41),(90,41),(91,41)), #Kiev
((63,32),(63,39),(63,40),(63,41),(64,41),(72,32),(73,32),(74,32),(75,32),(75,41),(76,32),(76,40),(76,41),(77,32),(77,39),(77,40),(77,41)), #Hungary
((25,26),(25,27),(25,28),(25,29),(25,30),(25,31),(34,36)), #Spain
(), #Denmark
((34,69),), #Scotland
((63,43),(63,44),(63,45),(64,43),(64,44),(65,43)), #Poland
(), #Genoa
(), #Morocco
((32,55),(32,56),(32,57),(32,58),(32,59),(32,60),(32,61),(32,62),(33,56),(33,57),(33,58),(33,59),(33,60),(33,61),(33,62)), #England
((25,21),(25,22),(25,23),(25,24),(25,25),(25,26),(25,32)), #Portugal
(), #Aragon
((60,59),(60,60),(60,61),(60,70),(60,71),(60,72),(61,59),(61,60),(61,72),(70,59),(70,60),(70,61),(71,59),(71,60),(71,61),(72,59),(72,60),(72,61),(73,59),(73,60),(73,61),(73,62),(74,59),(74,60),(74,61),(74,62),(74,63),(75,59),(75,60),(75,61),(75,62),(75,63)), #Sweden
((59,55),(60,55),(61,55),(63,48),(63,49),(63,50),(64,48),(64,49),(64,50),(65,48),(65,49),(65,50),(66,48),(66,49),(66,50),(67,48),(67,49),(67,50),(68,48),(68,49),(68,50),(69,48),(69,49),(69,50),(70,48),(70,49),(70,50),(71,48),(71,49),(71,50),(71,55)), #Prussia
((70,51),(70,52),(70,53),(70,54),(70,55),(70,59),(70,60),(70,61),(70,62),(70,63),(71,51),(71,52),(71,53),(71,54),(71,60),(71,61),(71,62),(71,63),(72,51),(72,60),(72,61),(72,62),(72,63),(73,63),(77,59),(77,60),(77,61),(77,62),(77,63)), #Lithuania
((57,36),(57,37),(58,36),(58,37),(59,36),(63,36),(63,37),(63,38)), #Austria
((76,27),(77,27),(78,27),(79,27),(80,27)), #Turkey
((83,59),(83,60),(83,61),(83,62),(83,63),(84,61),(84,62),(84,63),(85,62),(85,63),(86,63),(87,63),(88,63)), #Moscow
((51,50),(52,50)), #Dutch
()
)

#BroaderAreas: Used in civ birth only
tBroaderAreasTL = (
(68, 14), #Byzantium
(39, 41), #France
(92,  7), #Arabia
(71, 28), #Bulgaria
(24, 23), #Cordoba
(52, 29), #Venice
(42, 36), #Burgundy
(49, 41), #Germany
(77, 59), #Novgorod
(53, 63), #Norway
(81, 37), #Kiev
(64, 27), #Hungary
(23, 31), #Spain
(55, 55), #Denmark
(31, 57), #Scotland
(64, 42), #Poland
(45, 29), #Genoa
(11,  2), #Morocco
(38, 49), #England
(17, 27), #Portugal
(33, 25), #Aragon
(60, 58), #Sweden
(59, 49), #Prussia
(68, 45), #Lithuania
(56, 35), #Austria
(83, 17), #Turkey
(83, 51), #Moscow
(44, 47), #Dutch
(54, 25)  #Pope
)

tBroaderAreasBR = (
(83, 27), #Byzantium
(49, 51), #France
(99, 15), #Arabia
(80, 31), #Bulgaria
(34, 33), #Cordoba
(62, 39), #Venice
(52, 46), #Burgundy
(58, 51), #Germany
(89, 72), #Novgorod
(61, 72), #Norway
(91, 47), #Kiev
(74, 37), #Hungary
(33, 41), #Spain
(59, 60), #Denmark
(45, 69), #Scotland
(74, 52), #Poland
(55, 39), #Genoa
(29, 27), #Morocco
(48, 59), #England
(27, 37), #Portugal
(43, 34), #Aragon
(77, 72), #Sweden
(72, 55), #Prussia
(82, 64), #Lithuania
(66, 45), #Austria
(93, 27), #Turkey
(93, 61), #Moscow
(54, 57), #Dutch
(58, 29)  #Pope
)

#Visible Area: One or more rectangles.
tVisible = ((
#500 AD
( (64, 0,99,34),(49, 1,63,38),(24,13,48,36), ), # Byzantium
( (35,31,52,51),(49,26,59,38), ), # France
( (79, 0,89, 6),(90, 0,99,22), ), # Arabia
( (69,23,81,32),(78,31,99,41), ), # Bulgaria
( (18,13,39,33),(40, 0,59,20),(60, 0,95, 7), ), # Cordoba
( (47,14,59,38),(60,18,63,35),(64,18,68,29), ), # Venice
( (43,31,53,53), ), # Burgundy
( (44,31,46,52),(47,27,61,55),(62,50,70,55), ), # Germany
( (72,55,90,72),(79,41,88,54), ), # Novgorod
( (49,52,71,72),(30,56,48,72), ), # Norway
( (77,24,82,40),(83,33,88,46),(77,39,91,56), ), # Kiev
( (59,30,82,42),(83,36,92,42), ), # Hungary
( (22,25,35,38),(36,25,43,40), ), # Spain
( (34,46,49,72),(50,50,71,72),(72,57,78,64), ), # Denmark
( (30,51,46,72),(35,46,46,50), ), # Scotland
( (60,40,74,55),(75,40,79,48), ), # Poland
( (39,20,60,38),(47,14,63,32),(64,16,67,29), ), # Genoa
( (12, 2,42,31),(43,10,53,20), ), # Morocco
( (31,49,45,64),(37,46,45,48), ), # England
( (18,22,34,39), ), # Portugal
( (19,23,56,40),(25,21,45,22),(46,14,63,28), ),# Aragon
( (39,52,82,66),(34,61,71,72), ), # Sweden
( (51,43,73,56),(66,57,82,62),(69,63,79,66), ), # Prussia
( (67,46,76,55),(73,44,81,58), ), # Lithuania
( (49,27,61,55),(62,34,67,46), ), # Austria
( (75,13,99,27),(92, 4,99,12), ), # Turkey
( (77,42,99,51),(74,52,99,67), ), # Moscow
( (40,45,65,57),(49,58,67,66),(46,39,63,44), ), # Dutch
( (39,12,73,44), ), # Pope
),
#1200 AD
(
( (64, 0,99,34),(49, 1,63,38),(24,13,48,36), ), # Byzantium
( (30,26,59,54),(35,55,40,70), ), # France
( (26,20,35,23),(22, 5,27,19),(28, 9,53,19),(47, 0,85, 8),(86, 0,99,20), ), # Arabia
( (65,12,83,38),(78,31,99,41), ), # Bulgaria
( (18,13,39,33),(40, 0,59,20),(60, 0,95, 7), ), # Cordoba
( (46,14,70,41),(49, 7,82,25),(83, 7,91,13), ), # Venice
( (43,31,53,53), ), # Burgundy
( (41,31,61,58),(47,27,61,30),(62,34,70,55),(55,22,61,26), ), # Germany
( (72,55,90,72),(79,41,88,54),(91,60,99,72), ), # Novgorod
( (30,52,71,72),( 0,67,29,72), ), # Norway
( (75,42,94,62),(77,31,94,41),(77,24,82,40), ), # Kiev
( (56,27,82,45),(83,31,92,42),(65,12,82,26), ), # Hungary
( (20,17,56,40), ), # Spain
( (34,46,71,72),(72,57,78,72), ), # Denmark
( (30,43,46,72), ), # Scotland
( (60,37,79,60), ), # Poland
( (39,15,60,39),(47, 9,82,25),(61,26,67,32), ), # Genoa
( (12, 2,42,31),(43,2,53,20), ), # Morocco
( (26,54,46,64),(31,34,46,53), ), # England
( (18,17,34,39), ), # Portugal
( (19,29,56,40),(19,21,34,28),(35,14,63,28), ),# Aragon
#Below same as 500 AD
( (39,52,82,66),(34,61,71,72), ), # Sweden
( (51,43,73,56),(66,57,82,62),(69,63,79,66), ), # Prussia
( (67,46,76,55),(73,44,81,58), ), # Lithuania
( (49,27,61,55),(62,34,67,46), ), # Austria
( (75,13,99,27),(92, 4,99,12), ), # Turkey
( (77,42,99,51),(74,52,99,67), ), # Moscow
( (40,45,65,57),(49,58,67,66),(46,39,63,44), ), # Dutch
( (39,12,73,44), ), # Pope
))


# 3Miro: Initial Wars, note only the upper triangle of the array is valid, the lower should be all zeros
tWarAtSpawn = ((
# 500 AD
#Byz Fra Ara Bul Cor Ven Bur Ger Nov Nor Kie Hun Spn Den Sco Pol Gen Mor Eng Por Arg Swe Pru Lit Aus Tur Mos Dut Pop In1 In2 In3 In4
( 0,  0, 90, 90,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 90,  0,  0,  0,  0,  0,  0,  0, ), #Byz
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 60,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Fra
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 60,  0,  0,  0,  0,  0,  0,  0, ), #Ara
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 70,  0,  0,  0,  0,  0,  0,  0, ), #Bul
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 90,  0,  0,  0,  0,  0,  0, 90, 80,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Cor
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Ven
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Bur
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Ger
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 80,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Nov
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Nor
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Kie
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Hun
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Spn
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 60,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Den
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 60,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Sco
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 20,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Pol
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Gen
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Mor
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Eng
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Por
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Arg
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Swe
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  80, 0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Pru
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Lit
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Aus
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 50, 50, 50, 50, ), #Tur
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Mos
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Dut
),
(
# 1200 AD
#Byz Fra Ara Bul Cor Ven Bur Ger Nov Nor Kie Hun Spn Den Sco Pol Gen Mor Eng Por Arg Swe Pru Lit Aus Tur Mos Dut Pop In1 In2 In3 In4
( 0,  0, 20, 70,  0, 90,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 90,  0,  0,  0,  0,  0,  0,  0, ), #Byz
( 0,  0, 30,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 90,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Fra
( 0,  0,  0,  0,  0,  0,  0, 20,  0,  0,  0, 20, 30,  0,  0,  0, 20,  0, 20, 20, 10,  0,  0,  0,  0, 60,  0,  0,  0,  0,  0,  0,  0, ), #Ara
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 70,  0,  0,  0,  0,  0,  0,  0, ), #Bul
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 90,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Cor
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Ven
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Bur
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Ger
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 80,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Nov
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Nor
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Kie
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Hun
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Spn
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 60,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Den
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 60,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Sco
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 20,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Pol
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Gen
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 90,  0,  0,  0,  0,  0,  0, 80, 80,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Mor
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Eng
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Por
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Arg
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Swe
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  80, 0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Pru
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Lit
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Aus
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 50, 50, 50, 50, ), #Tur
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Mos
( 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, ), #Dut
))

#Congresses. # 3Miro: there is no congress, maybe I should remove this
tPatienceThreshold = (
30, #Byzantium
30, #Frankia
30, #Arabia
30, #Bulgaria
30, #Cordoba
30, #Venezia
30, #Burgundy
30, #Germany
30, #Novgorod
30, #Norway
30, #Kiev
30, #Hungary
30, #Spain
30, #Denmark
30, #Scotland
30, #Poland
30, #Genoa
30, #Morocco
30, #England
30, #Portugal
30, #Aragon
30, #Sweden
30, #Prussia
30, #Lithuania
30, #Austria
30, #Turkey
30, #Moscow
30  #Dutch
)


# religion spread modifiers:
tReligionSpreadFactor = ( # PROT, ISL, CATH, ORTH, JUD
(100,  50,  70, 150,  10), #Byzantium
(150,  20, 250,  70,  10), #France
( 20, 350,  50,  10,  10), #Arabia
( 80,  50,  80, 400,  10), #Bulgaria
( 50, 250,  80,  20,  10), #Cordoba
( 90,  50, 200,  30,  10), #Venezia
(150,  20, 150,  70,  10), #Burgundy
(450,  20, 250,  20,  10), #Germany
( 60,  40,  60, 500,  10), #Novgorod
(250,  50, 150,  80,  10), #Norway
( 90,  60,  90, 400,  10), #Kiev
(250,  60, 200,  80,  10), #Hungary
(100,  20, 200,  20,  10), #Spain
(250,  50, 180,  80,  10), #Denmark
(450,  20, 100,  20,  10), #Scotland
(200,  60, 450, 200,  10), #Poland
(190,  50, 250,  30,  10), #Genoa
( 50, 250,  70,  20,  10), #Morocco
(450,  20, 100,  20,  10), #England
(200,  80, 250,  20,  10), #Portugal
(150,  80, 250,  20,  10), #Aragon
(450,  20, 200,  50,  10), #Sweden
(450,  20, 250,  20,  10), #Prussia
( 80,  80,  80,  80,  10), #Lithuania
(200,  20, 250,  20,  10), #Austria
( 20, 350,  80,  80,  10), #Turkey
(100,  20, 100, 250,  10), #Moscow
(550,  20,  90,  20,  10), #Dutch
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
	(xml.iIslam, xml.iJudaism, xml.iCatholicism, xml.iProtestantism),		# Orthodoxy
	(xml.iIslam, xml.iProtestantism, xml.iOrthodoxy, xml.iCatholicism),		# Judaism
)


# 100 and 80: don't purge any religions; 60: purge islam if christian, and all christian religions if muslim; 40: also judaism; 20: all but state religion
tReligiousTolerance = (
60, #Byzantium
40, #Frankia
60, #Arabia
40, #Bulgaria
80, #Cordoba
40, #Venezia
20, #Burgundy
20, #Germany
60, #Novgorod
60, #Norway
40, #Kiev
60, #Hungary
20, #Spain
60, #Denmark
40, #Scotland
80, #Poland
20, #Genoa
60, #Morocco
40, #England
40, #Portugal
60, #Aragon
60, #Sweden
20, #Prussia
80, #Lithuania
20, #Austria
80, #Turkey
40, #Moscow
40, #Dutch
20, #Pope
100, #Indy1
100, #Indy2
100, #Indy3
100, #Indy4
100, #Barbarian
)


#Absinthe: old stability system, not used currently
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


#Lake name IDs (the actual names are in the corresponding GameText file, based on the ID we set here)
#More information about them in the Lakes of RFCEurope text file in the Reference folder
lLakeNameIDs = [
(32, 61,  0), #Lough Neagh
(64, 36,  1), (65, 36,  1), #Lake Balaton
(94,  4,  2), (94,  5,  2), #Dead Sea
(95,  8,  3), #Sea of Galilee
(88, 19,  4), (89, 19,  4), #Lake Tuz
(85, 18,  5), #Lake Egirdir
(86, 17,  6), #Lake Beysehir
(54, 37,  7), #Lake Garda
(49, 39,  8), #Lake Geneva
(53, 40,  9), #Lake Constance (Bodensee)
(66, 27, 10), #Lake Scutari (Lake Skadar)
(69, 23, 11), #Lake Ohrid (with Lake Prespa)
(71, 52, 12), #Lake Sniardwy (Spirdingsee)
(62, 62, 13), (62, 63, 13), #Lake Vättern
(60, 64, 14), (61, 64, 14), (61, 65, 14), #Lake Vänern
(64, 64, 15), (65, 64, 15), #Lake Mälaren (with Lake Hjälmaren)
(62, 71, 16), #Lake Storsjön
(77, 60, 17), (77, 61, 17), (77, 62, 17), #Lake Peipus
(80, 61, 18), #Lake Ilmen
(79, 67, 19), (79, 68, 19), (80, 65, 19), (80, 66, 19), (80, 67, 19), (80, 68, 19), (80, 69, 19), (81, 66, 19), (81, 67, 19), (81, 68, 19), #Lake Ladoga
(84, 69, 20), (84, 70, 20), (85, 68, 20), (85, 69, 20), (85, 70, 20), #Lake Onega
(87, 66, 21), #Lake Beloye
(77, 68, 22), (77, 69, 22), (78, 70, 22), #Lake Saimaa
(74, 68, 23), (74, 69, 23), #Lake Päijänne
(85, 72, 24), #Lake Vygozero
(83, 72, 25), #Lake Segozero
(76, 71, 26), #Lake Kallavesi (with Lake Suvasvesi and other smaller lakes in the area)
(74, 71, 27), #Lake Keitele (with many smaller lakes in the area)
(78, 72, 28), #Lake Pielinen
(72, 68, 29), #Lake Näsijärvi (with many smaller lakes in the area)
(55, 59, 30), #Limfjord (Limfjorden)
(58, 71, 31), #Trondheim Fjord (Trondheimsfjorden)
]


#Positions on the Colony map for "home" original flags
home_positions_xy = [
(578,179), #iByzantium
(480,152), #iFrankia
(614,212), #iArabia
(567,166), #iBulgaria
(455,195), #iCordoba
(518,157), #iVenecia
(490,160), #iBurgundy
(510,140), #iGermany
(580,103), #iNovgorod
(509,102), #iNorway
(590,140), #iKiev
(550,155), #iHungary
(460,180), #iSpain
(515,118), #iDenmark
(466,115), #iScotland
(540,130), #iPoland
(503,165), #iGenoa
(444,228), #iMorocco
(473,132), #iEngland
(441,190), #iPortugal
(470,182), #iAragon
(531, 92), #iSweden
(545,131), #iPrussia
(556,119), #iLithuania
(535,150), #iAustria
(590,195), #iTurkey
(595,110), #iMoscow
(492,131), #iDutch
]

#Positions on the Colony map where to display colonies
colony_positions_xy=[
(0,0), #Dummy slots for non-colony projects
(0,0),
(0,0),
(275,150), #Vinland
(480,335), #GoldCoast
(440,335), #IvoryCoast
(145,265), #Cuba
(185,280), #Hispaniola
(290,410), #Brazil
(160,110), #Hudson
(170,210), #Virginia
(610,390), #EastAfrica
(875,225), #China
(760,260), #India
(930,360), #East Indies
(870,320), #Malaysia
(560,510), #CapeTown
( 60,260), #Aztecs
(170,420), #Inca
(245,120), #Quebec
(200,180), #New England
(155,285), #Jamaica
(130,325), #Panama
(110,220), #Louisiana
(960,320), #Philippines
]


tLeaders = (		#First has to be the primary leader (the one that appears on the civ selection screen). Can be changed in the WB file (AbsintheRed)
(xml.iJustinian, xml.iBasil_II, xml.iPalaiologos),
(xml.iCharlemagne, xml.iPhilip_Augustus, xml.iJoan, xml.iLouis_Xiv),
(xml.iAbu_Bakr, xml.iHarun_al_Rashid, xml.iSaladin),
(xml.iSimeon, xml.iIvan_Asen),
(xml.iAbd_ar_Rahman, xml.iMohammed_ibn_Nasr),
(xml.iEnrico_Dandolo, xml.iAndrea_Gritti),
(xml.iOtto_William, xml.iBeatrice, xml.iPhilip_the_Bold),
(xml.iOtto_I, xml.iBarbarossa),
(xml.iRurik, xml.iAlexander_Nevsky, xml.iMarfa),
(xml.iHarald_Hardrada, xml.iHaakon_Iv),
(xml.iYaroslav, xml.iMstislav, xml.iBohdan_Khmelnytsky),
(xml.iStephen, xml.iBela_III, xml.iMatthias),
(xml.iFerdinand_III, xml.iIsabella, xml.iPhilip_Ii),
(xml.iHarald_Bluetooth, xml.iMargaret_I, xml.iChristian_Iv),
(xml.iRobert_the_Bruce, xml.iJames_IV),
(xml.iMieszko, xml.iCasimir, xml.iSobieski),
(xml.iEmbriaco, xml.iBoccanegra),
(xml.iYaqub_al_Mansur, xml.iIsmail_ibn_Sharif),
(xml.iWilliam, xml.iElizabeth, xml.iGeorge_Iii),
(xml.iAfonso, xml.iJoao, xml.iMaria_I),
(xml.iJames_I, xml.iJohn_II),
(xml.iMagnus_Ladulas, xml.iGustav_Vasa, xml.iGustav_Adolf, xml.iKarl_Xii),
(xml.iHermann_von_Salza, xml.iFrederick,),
(xml.iMindaugas, xml.iVytautas),
(xml.iMaximilian, xml.iMaria_Theresa),
(xml.iMehmed, xml.iSuleiman),
(xml.iIvan_Iv, xml.iPeter, xml.iCatherine),
(xml.iWillem_Van_Oranje, xml.iJohan_de_Witt),
(xml.iThe_Pope,)
)


tEarlyLeaders = (		#Don't have to be the same as the primary leader (AbsintheRed)
(xml.iJustinian),
(xml.iCharlemagne),
(xml.iAbu_Bakr),
(xml.iSimeon),
(xml.iAbd_ar_Rahman),
(xml.iEnrico_Dandolo),
(xml.iOtto_William),
(xml.iOtto_I),
(xml.iRurik),
(xml.iHarald_Hardrada),
(xml.iYaroslav),
(xml.iStephen),
(xml.iFerdinand_III),
(xml.iHarald_Bluetooth),
(xml.iRobert_the_Bruce),
(xml.iMieszko),
(xml.iEmbriaco),
(xml.iYaqub_al_Mansur),
(xml.iWilliam),
(xml.iAfonso),
(xml.iJames_I),
(xml.iMagnus_Ladulas),
(xml.iHermann_von_Salza),
(xml.iMindaugas),
(xml.iMaximilian),
(xml.iMehmed),
(xml.iIvan_Iv),
(xml.iWillem_Van_Oranje),
(xml.iThe_Pope)
)


tLateLeaders = (		#The switch is triggered after a few years (starting date, percentage, era)
((xml.iBasil_II, xml.i910AD, 10, 2), (xml.iPalaiologos, xml.i1230AD, 5, 2),),
((xml.iPhilip_Augustus, xml.i1101AD, 10, 2), (xml.iJoan, xml.i1376AD, 10, 2), (xml.iLouis_Xiv, xml.i1523AD, 25, 3),),
((xml.iHarun_al_Rashid, xml.i752AD, 25, 1), (xml.iSaladin, xml.i1160AD, 25, 2),),
((xml.iIvan_Asen, xml.i1101AD, 10, 2),),
((xml.iMohammed_ibn_Nasr, xml.i1202AD, 10, 2),),
((xml.iAndrea_Gritti, xml.i1259AD, 10, 2),),
((xml.iBeatrice, xml.i1200AD, 10, 2), (xml.iPhilip_the_Bold, xml.i1356AD, 15, 2),),
((xml.iBarbarossa, xml.i1139AD, 20, 2),),
((xml.iAlexander_Nevsky, xml.i1150AD, 10, 2), (xml.iMarfa, xml.i1380AD, 10, 3),),
((xml.iHaakon_Iv, xml.i1160AD, 25, 2),),
((xml.iMstislav, xml.i1101AD, 5, 2), (xml.iBohdan_Khmelnytsky, xml.i1520AD, 10, 3),),
((xml.iBela_III, xml.i1167AD, 15, 2), (xml.iMatthias, xml.i1444AD, 5, 3),),
((xml.iIsabella, xml.i1250AD, 10, 2), (xml.iPhilip_Ii, xml.i1520AD, 10, 3),),
((xml.iMargaret_I, xml.i1320AD, 10, 2), (xml.iChristian_Iv, xml.i1520AD, 5, 3),),
((xml.iJames_IV, xml.i1296AD, 10, 2),),
((xml.iCasimir, xml.i1320AD, 20, 2), (xml.iSobieski, xml.i1570AD, 10, 3),),
((xml.iBoccanegra, xml.i1101AD, 10, 2),),
((xml.iIsmail_ibn_Sharif, xml.i1419AD, 5, 3),),
((xml.iElizabeth, xml.i1452AD, 10, 3), (xml.iGeorge_Iii, xml.i1700AD, 10, 3),),
((xml.iJoao, xml.i1419AD, 10, 3), (xml.iMaria_I, xml.i1700AD, 10, 3),),
((xml.iJohn_II, xml.i1397AD, 15, 3),),
((xml.iGustav_Vasa, xml.i1470AD, 20, 3), (xml.iGustav_Adolf, xml.i1540AD, 25, 3), (xml.iKarl_Xii, xml.i1680AD, 10, 3),),
((xml.iFrederick, xml.i1580AD, 5, 3),),
((xml.iVytautas, xml.i1377AD, 10, 3),),
((xml.iMaria_Theresa, xml.i1700AD, 25, 3),),
((xml.iSuleiman, xml.i1520AD, 15, 3),),
((xml.iPeter, xml.i1570AD, 10, 3), (xml.iCatherine, xml.i1700AD, 25, 3),),
((xml.iJohan_de_Witt, xml.i1650AD, 30, 3),),
((xml.iThe_Pope,),)
)


# Absinthe: UP initialization

iUP_Happiness = 0					# happiness bonus
iUP_PerCityCommerce = 1				# commerce bonus per city
iUP_CityTileYield = 2				# yield bonus on the city tile
iUP_ReligiousTolerance = 3			# no instability from foreign religion
iUP_CulturalTolerance = 4			# no unhappiness from foreign culture
iUP_CommercePercent = 5				# global bonus to specific type of commerce - currently unused
iUP_UnitProduction = 6				# after specific tech, faster unit production
iUP_EnableCivics = 7				# always enable some civics (also use the WB)
iUP_TradeRoutes = 8					# add some trade routes (sync with GlobalDefines.xml for max trade routes)
iUP_ImprovementBonus = 9			# change the yield of a specific improvement
iUP_PromotionI = 10					# give a promotion to all units for which it is valid
iUP_PromotionII = 11				# give a promotion to all units regardless if it is valid - currently unused
iUP_CanEnterTerrain = 12			# all units can enter the specified terrain type
iUP_NoResistance = 13				# no resistance in conquered cities
iUP_Conscription = 14				# can draft from cities with foreign culture - currently unused
iUP_Inquisition = 15				# less instability from religious prosecution
iUP_Emperor = 16					# no collapse/civil war and no city secession in core+normal areas, if you hold your historic capital (Python only)
iUP_Faith = 17						# state religion spreads to newly acquired cities (found/trade/conquest) with a temple (Python only)
iUP_Mercenaries = 18				# halves the cost of mercenaries (Python only)
iUP_LandStability = 19				# less stability penalty from owning unstable land (Python only)
iUP_Discovery = 20					# lower cost for the specified projects
iUP_EndlessLand = 21				# lower city maintenance costs from both number of cities and city distance, also lower civic costs associated with cities
iUP_ForeignSea = 22					# allows ships to enter foreign sea territory - currently unused (this is allowed by default for all civs' all naval units)
iUP_Pious = 23						# increase the gain (and loss) of Faith Points
iUP_PaganCulture = 24				# give bonus to culture if no state religion is present
iUP_PaganHappy = 25					# give bonus to happiness if no state religion is present
iUP_HealthFood = 26					# positive health contributes to city growth
iUP_TerrainBonus = 27				# add bonus to one or more types of yield for a specific terrain
iUP_FeatureBonus = 28				# add bonus to one or more types of yield for a specific feature
iUP_StabilityConquestBoost = 29		# if stability is < 0, then get +1 stability on Conquest - currently unused
iUP_StabilitySettler = 30			# don't lose stability from founding cities in Contested (border/outer/ok) and Foreign (unstable) Provinces - currently unused
iUP_StabilityPlaceholder1 = 31		# currently unused
iUP_StabilityPlaceholder2 = 32		# currently unused
iUP_Janissary = 33					# free units for foreign religions (Python only)
iUP_ImprovementBonus2 = 34			# change the yield of a specific improvement - in order to have bonuses for multiple improvements
iUP_ImprovementBonus3 = 35			# change the yield of a specific improvement - in order to have bonuses for multiple improvements
iUP_ImprovementBonus4 = 36			# change the yield of a specific improvement - in order to have bonuses for multiple improvements
iUP_ImprovementBonus5 = 37			# change the yield of a specific improvement - in order to have bonuses for multiple improvements
# the following are entirely in python, not even added in the .dll as enums (CvRhyes.h)
iUP_SoundToll = 38					# gold for coastal cities in a region if the entry strait is controlled (Python only)
iUP_NoAnarchyInstability = 39		# no anarchy instability on civic or religion change (Python only)
iUP_ProvinceCommerce = 40			# extra commerce in capital for each controlled province (Python only)
iUP_Defiance = 41					# extra units in all cities when a city is lost (Python only)


iFP_Stability = 0		# stability bonus
iFP_Civic = 1			# lower civic upkeep
iFP_Growth = 2			# faster population growth
iFP_Units = 3			# lower production cost for units
iFP_Science = 4			# lower beaker cost for new techs
iFP_Production = 5		# lower cost for Wonders and Projects
iFP_Diplomacy = 6		# diplomacy boost


# Saint section
iSaintBenefit = 8		# number of Faith points generated by a saint

# Crusade section / Towns
iNumCrusades = 6
tJerusalem = ( 93, 5 )

# Province Status
iProvinceOwn = 5      # own every tile
iProvinceConquer = 4  # own every city (capture or settle) or own every tile
iProvinceDominate = 3 # 2*sum of population + owned tiles is more for you than the sum total of everyone else (True if conquer is True)
iProvinceLost = 2     # you have no cities and others have cities in it

# ProvinceTypes
iProvinceNone      = 0 # this is the default, use it for everything too far away to be considered
iProvinceOuter     = 1 # small stability hit on owning
iProvincePotential = 2 # changes to Core or Natural as soon as conquered - only to Natural currently
iProvinceNatural   = 3 # stable, small penalty for not conquering it
iProvinceCore      = 4 # stable, large penalty for not conquering it
iNumProvinceTypes  = 5

# special parameters 10 per player (picklefree)
iIsHasStephansdom     = 0 # Stability parameter in Python
iIsHasEscorial        = 1 # Stability parameter in Python
iMercCostPerTurn      = 2 # Mercenaries
iJanissaryPoints      = 3 # Janissary points
iIsHasUppsalaShrine   = 4 # Stability parameter in Python
iIsHasKoutoubiaMosque = 5 # Stability parameter in Python
iIsHasMagnaCarta      = 6 # Stability parameter in Python
iIsHasGalataTower     = 7 # Company parameter in Python

# Stability categories
iCathegoryCities = 0
iCathegoryCivics = 1
iCathegoryEconomy = 2
iCathegoryExpansion = 3
