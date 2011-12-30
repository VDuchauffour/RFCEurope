# Rhye's and Fall of Civilization - Mercenaries Written mostly by 3Miro
from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
import cPickle as pickle
import Consts as con
import XMLConsts as xml

#from sets import Set

iNumPlayers = con.iNumPlayers

iMercPromotion = xml.iPromotionMerc

#PyGame = PyHelpers.PyGame()

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

iMercCostPerTurn = con.iMercCostPerTurn

# list of all available mercs, unit type, text key name, start turn, end turn, provinces, blocked by religions, odds
# note that the province list is treated as a set (only iProvince in list or Set(list) are ever called)
# the odds show the odds of the merc to appear every turn, this is nothing more than a delay on when the merc would appear (90-100 means right at the date, 10-30 should be good for most mercs)
lMercList = [   [xml.iAxeman, "TXT_KEY_MERC_SERBIAN", 60, 108, xml.lRegionBalkans, [], 20 ],
                [xml.iArcher, "TXT_KEY_MERC_SERBIAN", 60, 108, xml.lRegionBalkans, [], 20 ],
                [xml.iHorseArcher, "TXT_KEY_MERC_KHAZAR", 25, 90, xml.lRegionBalkans + [xml.iP_Constantinople], [], 20 ],
                [xml.iHorseArcher, "TXT_KEY_MERC_KHAZAR", 25, 108, xml.lRegionBalkans + [xml.iP_Constantinople], [], 20 ],
                [xml.iHorseArcher, "TXT_KEY_MERC_AVAR", 25, 75, xml.lRegionBalkans + xml.lRegionAustria + xml.lRegionHungary + [xml.iP_Constantinople], [], 20 ],
                [xml.iHorseArcher, "TXT_KEY_MERC_AVAR", 25, 75, xml.lRegionBalkans + xml.lRegionAustria + xml.lRegionHungary + [xml.iP_Constantinople], [], 20 ],
                [xml.iMountedInfantry, "TXT_KEY_MERC_GENERIC", 50, 80, xml.lRegionFrance, [], 20 ],
                [xml.iMountedInfantry, "TXT_KEY_MERC_GENERIC", 50, 80, xml.lRegionGermany, [], 20 ],
                [xml.iMountedInfantry, "TXT_KEY_MERC_GENERIC", 50, 80, xml.lRegionIberia, [], 20 ],
                [xml.iArcher, "TXT_KEY_MERC_GENERIC", 50, 80, xml.lRegionFrance, [], 20 ],
                [xml.iArcher, "TXT_KEY_MERC_GENERIC", 50, 80, xml.lRegionGermany, [], 20 ],
                [xml.iArcher, "TXT_KEY_MERC_GENERIC", 50, 80, xml.lRegionIberia, [], 20 ],
                [xml.iCrossbowman, "TXT_KEY_MERC_GENERIC", 100, 200, xml.lRegionFrance, [], 20 ],
                [xml.iCrossbowman, "TXT_KEY_MERC_GENERIC", 100, 200, xml.lRegionGermany, [], 20 ],
                [xml.iCrossbowman, "TXT_KEY_MERC_GENERIC", 100, 200, xml.lRegionIberia, [], 20 ],
                [xml.iCrossbowman, "TXT_KEY_MERC_GENERIC", 100, 200, xml.lRegionBritain, [], 20 ],
                [xml.iCrossbowman, "TXT_KEY_MERC_GENERIC", 100, 200, xml.lRegionPoland, [], 20 ],
                [xml.iCrossbowman, "TXT_KEY_MERC_GENERIC", 100, 200, xml.lRegionHungary, [], 20 ],
                [xml.iCrossbowman, "TXT_KEY_MERC_GENERIC", 100, 200, xml.lRegionMiddleEast, [], 20 ],
                [xml.iLongbowman, "TXT_KEY_MERC_GENERIC", 200, 300, xml.lRegionFrance, [], 20 ],
                [xml.iLongbowman, "TXT_KEY_MERC_GENERIC", 200, 300, xml.lRegionGermany, [], 20 ],
                [xml.iLongbowman, "TXT_KEY_MERC_GENERIC", 200, 300, xml.lRegionIberia, [], 20 ],
                [xml.iLongbowman, "TXT_KEY_MERC_GENERIC", 200, 300, xml.lRegionBritain, [], 20 ],
                [xml.iLongbowman, "TXT_KEY_MERC_GENERIC", 200, 300, xml.lRegionBalkans, [], 20 ],
                [xml.iSpearman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionFrance, [], 20 ],
                [xml.iSpearman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionGermany, [], 20 ],
                [xml.iSpearman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionIberia, [], 20 ],
                [xml.iSpearman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionBritain, [], 20 ],
                [xml.iSpearman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionPoland, [], 20 ],
                [xml.iSpearman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionHungary, [], 20 ],
                [xml.iSpearman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionBalkans, [], 20 ],
                [xml.iSpearman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionKiev, [], 20 ],
                [xml.iSpearman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionMiddleEast, [], 20 ],
                [xml.iSwordsman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionFrance, [], 20 ],
                [xml.iSwordsman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionGermany, [], 20 ],
                [xml.iSwordsman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionIberia, [], 20 ],
                [xml.iSwordsman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionBritain, [], 20 ],
                [xml.iSwordsman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionPoland, [], 20 ],
                [xml.iSwordsman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionHungary, [], 20 ],
                [xml.iSwordsman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionBalkans, [], 20 ],
                [xml.iSwordsman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionKiev, [], 20 ],
                [xml.iSwordsman, "TXT_KEY_MERC_GENERIC", 50, 150, xml.lRegionMiddleEast, [], 20 ],
                [xml.iKnight, "TXT_KEY_MERC_GENERIC", 200, 300, xml.lRegionFrance, [], 20 ],
                [xml.iKnight, "TXT_KEY_MERC_GENERIC", 200, 300, xml.lRegionGermany, [], 20 ],
                [xml.iKnight, "TXT_KEY_MERC_GENERIC", 200, 300, xml.lRegionIberia, [], 20 ],
                [xml.iKnight, "TXT_KEY_MERC_GENERIC", 200, 300, xml.lRegionBritain, [], 20 ],
                [xml.iKnight, "TXT_KEY_MERC_GENERIC", 200, 300, xml.lRegionPoland, [], 20 ],
                [xml.iKnight, "TXT_KEY_MERC_GENERIC", 200, 300, xml.lRegionHungary, [], 20 ],
                [xml.iKnight, "TXT_KEY_MERC_GENERIC", 200, 300, xml.lRegionBalkans, [], 20 ],
                [xml.iKnight, "TXT_KEY_MERC_GENERIC", 200, 300, xml.lRegionKiev, [], 20 ],
                [xml.iKnight, "TXT_KEY_MERC_GENERIC", 200, 300, xml.lRegionMiddleEast, [], 20 ],
                [xml.iMusketman, "TXT_KEY_MERC_GENERIC", 300, 400, xml.lRegionFrance, [], 20 ],
                [xml.iMusketman, "TXT_KEY_MERC_GENERIC", 300, 400, xml.lRegionGermany, [], 20 ],
                [xml.iMusketman, "TXT_KEY_MERC_GENERIC", 300, 400, xml.lRegionIberia, [], 20 ],
                [xml.iMusketman, "TXT_KEY_MERC_GENERIC", 300, 400, xml.lRegionBritain, [], 20 ],
                [xml.iMusketman, "TXT_KEY_MERC_GENERIC", 300, 400, xml.lRegionPoland, [], 20 ],
                [xml.iMusketman, "TXT_KEY_MERC_GENERIC", 300, 400, xml.lRegionHungary, [], 20 ],
                [xml.iMusketman, "TXT_KEY_MERC_GENERIC", 300, 400, xml.lRegionBalkans, [], 20 ],
                [xml.iMusketman, "TXT_KEY_MERC_GENERIC", 300, 400, xml.lRegionKiev, [], 20 ],
                [xml.iMusketman, "TXT_KEY_MERC_GENERIC", 300, 400, xml.lRegionMiddleEast, [], 20 ],
                [xml.iTemplar, "TXT_KEY_KNIGHTS_TEMPLAR", 170, 300, xml.lRegionMiddleEast, [xml.iIslam, xml.iOrthodoxy, xml.iProtestantism], 50 ],
                [xml.iTemplar, "TXT_KEY_KNIGHTS_TEMPLAR", 170, 300, xml.lRegionMiddleEast, [xml.iIslam, xml.iOrthodoxy, xml.iProtestantism], 50 ],
				[xml.iTemplar, "TXT_KEY_KNIGHTS_TEMPLAR", 170, 300, [xml.iP_Jerusalem], [xml.iIslam, xml.iOrthodoxy, xml.iProtestantism], 50 ],
                [xml.iTeutonic, "TXT_KEY_TEUTONIC_KNIGHTS", 170, 300, xml.lRegionMiddleEast, [xml.iIslam, xml.iOrthodoxy, xml.iProtestantism], 50 ],
                [xml.iTeutonic, "TXT_KEY_TEUTONIC_KNIGHTS", 170, 300, xml.lRegionMiddleEast, [xml.iIslam, xml.iOrthodoxy, xml.iProtestantism], 50 ],
				[xml.iTeutonic, "TXT_KEY_TEUTONIC_KNIGHTS", 170, 300, [xml.iP_Jerusalem], [xml.iIslam, xml.iOrthodoxy, xml.iProtestantism], 50 ],
                [xml.iCondottieri, "TXT_KEY_MERC_ITALIAN", 217, 375, xml.lRegionItaly, [], 50 ],
                [xml.iCondottieri, "TXT_KEY_MERC_ITALIAN", 217, 375, xml.lRegionItaly, [], 50 ],
                [xml.iCondottieri, "TXT_KEY_MERC_ITALIAN", 217, 375, xml.lRegionItaly, [], 50 ],
                [xml.iSwissPikeman, "TXT_KEY_MERC_SWISS", 233, 313, xml.lRegionSwiss, [], 50 ],
                [xml.iSwissPikeman, "TXT_KEY_MERC_SWISS", 233, 313, xml.lRegionSwiss, [], 50 ],
                [xml.iSwissPikeman, "TXT_KEY_MERC_SWISS", 233, 313, xml.lRegionSwiss, [], 50 ],
                [xml.iSwissPikeman, "TXT_KEY_MERC_SWISS", 233, 313, xml.lRegionSwiss, [], 50 ],
                [xml.iVarangianGuard, "TXT_KEY_MERC_VARANGIAN", 128, 267, [xml.iP_Constantinople], [], 50 ],
                [xml.iVarangianGuard, "TXT_KEY_MERC_VARANGIAN", 128, 267, [xml.iP_Constantinople], [], 50 ],
                [xml.iHuscarl, "TXT_KEY_MERC_DANISH", 75, 200, xml.lRegionScandinavia, [], 50 ],
                [xml.iHuscarl, "TXT_KEY_MERC_DANISH", 75, 200, xml.lRegionScandinavia, [], 50 ],
                [xml.iHuscarl, "TXT_KEY_MERC_DANISH", 75, 200, xml.lRegionScandinavia, [], 50 ],
                [xml.iAlmogavar, "TXT_KEY_MERC_ARAGON", 188, 267, [xml.iP_Catalonia, xml.iP_Aragon, xml.iP_Valencia], [], 50 ],
                [xml.iAlmogavar, "TXT_KEY_MERC_ARAGON", 188, 267, [xml.iP_Catalonia, xml.iP_Aragon, xml.iP_Valencia], [], 50 ],
                [xml.iAlmogavar, "TXT_KEY_MERC_ARAGON", 234, 270, [xml.iP_Thessaly, xml.iP_Thessaloniki], [], 50 ],
                [xml.iBlackGuard, "TXT_KEY_MERC_MOROCCO", 375, 430, [xml.iP_Morocco, xml.iP_Oran, xml.iP_Tetouan, xml.iP_Marrakesh, xml.iP_Fez], [], 50 ],
                [xml.iBlackGuard, "TXT_KEY_MERC_MOROCCO", 375, 430, [xml.iP_Morocco, xml.iP_Oran, xml.iP_Tetouan, xml.iP_Marrakesh, xml.iP_Fez], [], 50 ],
                [xml.iHackapell, "TXT_KEY_MERC_FINNISH", 359, 500, [xml.iP_Osterland, xml.iP_Norrland, xml.iP_Karelia], [], 50 ],
                [xml.iHackapell, "TXT_KEY_MERC_FINNISH", 359, 500, [xml.iP_Osterland, xml.iP_Norrland, xml.iP_Karelia], [], 50 ],
                [xml.iReiter, "TXT_KEY_MERC_GERMAN", 350, 400, [xml.iP_Silesia, xml.iP_LesserPoland, xml.iP_Masovia, xml.iP_GreaterPoland, xml.iP_Pomerania], [], 50 ],
                [xml.iReiter, "TXT_KEY_MERC_GERMAN", 350, 400, [xml.iP_Silesia, xml.iP_LesserPoland, xml.iP_Masovia, xml.iP_GreaterPoland, xml.iP_Pomerania], [], 50 ],
                [xml.iReiter, "TXT_KEY_MERC_GERMAN", 350, 400, [xml.iP_Silesia, xml.iP_LesserPoland, xml.iP_Masovia, xml.iP_GreaterPoland, xml.iP_Pomerania], [], 50 ],
                [xml.iZaporozhianCossack, "TXT_KEY_MERC_ZAPOROZHIAN", 300, 500, [xml.iP_Zaporizhia, xml.iP_Kiev, xml.iP_Sloboda], [], 50 ],
                [xml.iZaporozhianCossack, "TXT_KEY_MERC_ZAPOROZHIAN", 300, 500, [xml.iP_Zaporizhia, xml.iP_Kiev, xml.iP_Sloboda], [], 50 ],
                [xml.iDonCossack, "TXT_KEY_MERC_DON", 350, 500, [xml.iP_Kuban, xml.iP_Donets], [], 50 ],
                [xml.iDonCossack, "TXT_KEY_MERC_DON", 350, 500, [xml.iP_Kuban, xml.iP_Donets], [], 50 ],
                [xml.iDoppelsoldner, "TXT_KEY_MERC_GERMAN", 300, 400, xml.lRegionGermany, [], 50 ],
                [xml.iDoppelsoldner, "TXT_KEY_MERC_GERMAN", 300, 400, xml.lRegionGermany, [], 50 ],
                [xml.iDoppelsoldner, "TXT_KEY_MERC_GERMAN", 300, 400, xml.lRegionGermany, [], 50 ],
                [xml.iIrishBrigade, "TXT_KEY_MERC_IRISH", 390, 500, [xml.iP_Ireland], [], 50 ],
                [xml.iIrishBrigade, "TXT_KEY_MERC_IRISH", 390, 500, [xml.iP_Ireland], [], 50 ],
                [xml.iStradiot, "TXT_KEY_MERC_BALKAN", 280, 430, xml.lRegionBalkans, [], 50 ],
                [xml.iStradiot, "TXT_KEY_MERC_BALKAN", 280, 430, xml.lRegionBalkans, [], 50 ],
                [xml.iWaardgelder, "TXT_KEY_MERC_BALKAN", 340, 450, [xml.iP_Netherlands, xml.iP_Flanders], [], 50 ],
                [xml.iWaardgelder, "TXT_KEY_MERC_BALKAN", 340, 450, [xml.iP_Netherlands, xml.iP_Flanders], [], 50 ],
                [xml.iNaffatun, "TXT_KEY_MERC_ARABIAN", 160, 217, xml.lRegionMiddleEast, [xml.iCatholicism, xml.iOrthodoxy, xml.iProtestantism], 50 ],
                [xml.iNaffatun, "TXT_KEY_MERC_ARABIAN", 160, 217, xml.lRegionMiddleEast, [xml.iCatholicism, xml.iOrthodoxy, xml.iProtestantism], 50 ],
                [xml.iTurkopoles, "TXT_KEY_MERC_EGYPTIAN", 160, 217, xml.lRegionMiddleEast + [xml.iP_Egypt], [xml.iIslam, xml.iOrthodoxy, xml.iProtestantism], 50 ],
                [xml.iTurkopoles, "TXT_KEY_MERC_EGYPTIAN", 160, 217, xml.lRegionMiddleEast + [xml.iP_Egypt], [xml.iIslam, xml.iOrthodoxy, xml.iProtestantism], 50 ],
                [xml.iWalloonGuard, "TXT_KEY_MERC_WALLOON", 434, 500, [xml.iP_Flanders, xml.iP_Lorraine, xml.iP_Picardy], [xml.iIslam, xml.iOrthodoxy, xml.iProtestantism], 50 ],
                [xml.iWalloonGuard, "TXT_KEY_MERC_WALLOON", 434, 500, [xml.iP_Flanders, xml.iP_Lorraine, xml.iP_Picardy], [xml.iIslam, xml.iOrthodoxy, xml.iProtestantism], 50 ],
                [xml.iSwissGun, "TXT_KEY_MERC_SWISS", 320, 500, xml.lRegionSwiss, [], 50 ],
                [xml.iSwissGun, "TXT_KEY_MERC_SWISS", 320, 500, xml.lRegionSwiss, [], 50 ],
                [xml.iSwissGun, "TXT_KEY_MERC_SWISS", 320, 500, xml.lRegionSwiss, [], 50 ],
                [xml.iSwissGun, "TXT_KEY_MERC_SWISS", 320, 500, xml.lRegionSwiss, [], 50 ],
                [xml.iLipkaTatar, "TXT_KEY_MERC_BALTIC", 240, 385, xml.lRegionLithuania + [xml.iP_Polotsk, xml.iP_Suvalkija, xml.iP_Minsk], [], 50 ],
                [xml.iLipkaTatar, "TXT_KEY_MERC_BALTIC", 240, 385, xml.lRegionLithuania + [xml.iP_Polotsk, xml.iP_Suvalkija, xml.iP_Minsk], [], 50 ],
                [xml.iHighlanderGun, "TXT_KEY_MERC_SCOTTISH", 380, 500, [xml.iP_Scotland], [], 50 ],
                [xml.iHighlanderGun, "TXT_KEY_MERC_SCOTTISH", 380, 500, [xml.iP_Scotland], [], 50 ],
                [xml.iZanji, "TXT_KEY_MERC_AFRICAN", 42, 200, xml.lRegionAfrica + [xml.iP_Egypt], [xml.iCatholicism, xml.iOrthodoxy, xml.iProtestantism], 50 ],
                [xml.iZanji, "TXT_KEY_MERC_AFRICAN", 42, 200, xml.lRegionAfrica + [xml.iP_Egypt], [xml.iCatholicism, xml.iOrthodoxy, xml.iProtestantism], 50 ],
                [xml.iZanji, "TXT_KEY_MERC_AFRICAN", 42, 200, xml.lRegionAfrica + [xml.iP_Egypt], [xml.iCatholicism, xml.iOrthodoxy, xml.iProtestantism], 50 ],
                [xml.iTouareg, "TXT_KEY_MERC_AFRICAN", 50, 266, [xml.iP_Morocco, xml.iP_Marrakesh, xml.iP_Tetouan, xml.iP_Oran, xml.iP_Fez], [xml.iCatholicism, xml.iOrthodoxy, xml.iProtestantism], 50 ],
                [xml.iTouareg, "TXT_KEY_MERC_AFRICAN", 50, 266, [xml.iP_Morocco, xml.iP_Marrakesh, xml.iP_Tetouan, xml.iP_Oran, xml.iP_Fez], [xml.iCatholicism, xml.iOrthodoxy, xml.iProtestantism], 50 ],
                [xml.iNubianLongbowman, "TXT_KEY_MERC_NUBIAN", 37, 150, [xml.iP_Egypt], [], 50 ],
                [xml.iNubianLongbowman, "TXT_KEY_MERC_NUBIAN", 37, 150, [xml.iP_Egypt], [], 50 ],
				[xml.iHighlander, "TXT_KEY_MERC_HIGHLANDER", 180, 370, [xml.iP_Scotland, xml.iP_Northumbria, xml.iP_TheIsles], [], 50 ],
				[xml.iHighlander, "TXT_KEY_MERC_HIGHLANDER", 180, 370, [xml.iP_Scotland, xml.iP_Northumbria, xml.iP_TheIsles], [], 50 ],
				[xml.iHighlander, "TXT_KEY_MERC_HIGHLANDER", 180, 370, [xml.iP_Scotland, xml.iP_Northumbria, xml.iP_TheIsles], [], 50 ],
				[xml.iWelshLongbowman, "TXT_KEY_MERC_WELSH", 200, 350, [xml.iP_Wales], [], 50 ],
				[xml.iWelshLongbowman, "TXT_KEY_MERC_WELSH", 200, 350, [xml.iP_Wales], [], 50 ],
				[xml.iTagmata, "TXT_KEY_MERC_TAGMATA", 120, 217, xml.lRegionAsiaMinor, [], 50 ],
				[xml.iTagmata, "TXT_KEY_MERC_TAGMATA", 120, 217, xml.lRegionAsiaMinor, [], 50 ],
				[xml.iTagmata, "TXT_KEY_MERC_TAGMATA", 120, 217, [xml.iP_Constantinople], [], 50 ],
				[xml.iCorsair, "TXT_KEY_MERC_CORSAIR", 260, 450, [xml.iP_Oran, xml.iP_Algiers, xml.iP_Ifriqiya, xml.iP_Cyrenaica, xml.iP_Tripolitania], [xml.iCatholicism, xml.iOrthodoxy, xml.iProtestantism], 50 ],
				[xml.iCorsair, "TXT_KEY_MERC_CORSAIR", 260, 450, [xml.iP_Oran, xml.iP_Algiers, xml.iP_Ifriqiya, xml.iP_Cyrenaica, xml.iP_Tripolitania], [xml.iCatholicism, xml.iOrthodoxy, xml.iProtestantism], 50 ],
				[xml.iCorsair, "TXT_KEY_MERC_CORSAIR", 260, 450, [xml.iP_Ifriqiya], [xml.iCatholicism, xml.iOrthodoxy, xml.iProtestantism], 50 ],
                ]

### A few Parameters for Mercs only:
# Promotions and their odds, higher promotions have very low probability, leaders and navigation don't appear
# combat 1 - 5, cover (vs archer), shock (vs heavy infantry), formation (vs heavy horse), charge (vs siege), ambush (vs light cav), feint (vs polearm), amphibious, march (movement heal), medic 1-2, 
# gurilla (hill defense) 1-3, woodsman 1-3, city raider 1-3, garrison 1-3, drill 1-4, barrage (collateral) 1-3, accuracy (more bombard), flanking (vs siege) 1-2, sentry (vision), mobility (movement), 
# navigation 1-2, leader, leadership (more XP), tactic (withdraw), commando (enemy roads), combat 6, morale (movement), medic 3, merc 
lPromotionOdds = [ 100, 80, 40, 10,  5, 50, 50, 60, 40, 20, 50, 20, 10, 40, 20, 80, 50, 30, 80, 50, 30, 80, 40, 10, 60, 30, 10, 60, 40, 10,  5, 60, 40, 10, 60, 50, 30, 20, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
# The way promotions would affect the cost of the mercenary (percentage wise)
lPromotionCost = [  10, 15, 30, 30, 40, 20, 20, 20, 20, 20, 20, 30, 40, 20, 30, 15, 20, 30, 15, 20, 30, 20, 30, 50, 20, 30, 50, 10, 20, 40, 50, 10, 10, 10, 20, 10, 10, 10, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
iNumTotalPromotions = 39 # without navigation and leaders
iNumPromotionsSoftCap = 3 # canget more promotions if you get a high promotion (i.e. combat 5), but overall it should be unlikely
iNumPromorionIterations = 3 # how many attemps shall we make to add promotion (the bigger the number, the more likely it is for a unit to have at least iNumPromotionsSoftCap promotions)

# 3MiroUP: set the merc cost modifiers here
lMercCostModifier = (
150,  # Byzantium
120,  # Frankia
100, # Arabia
100, # Bulgaria
100, # Cordoba
100, # Norse
100, # Venecia
100, # Burgundy
110, # Germany
100, # Kiev
100, # Hungary
100, # Spain
100, # Poland
50, # Genoa
100,# England
100,# Portugal
100,# Lithuania
100,# Austria
100,# Turkey
100,# Moscow 
100,# Sweden
100,# Dutch
0,	#Pope
0,
0,
0,
0,
0
) 

class MercenaryManager:

        def __init__(self ):
                self.lGlobalPool = []
                self.lHiredBy = []
                self.GMU = GlobalMercenaryUtils()
		pass

        def getMercLists(self):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                self.lGlobalPool = scriptDict['lMercGlobalPool']
                self.lHiredBy = scriptDict['lMercsHiredBy']
                
        def setMercLists( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lMercGlobalPool'] = self.lGlobalPool
                scriptDict['lMercsHiredBy'] = self.lHiredBy
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def rendomizeMercProvinces( self, iGameTurn ):
                if ( iGameTurn % 2 == gc.getGame().getSorenRandNum( 2, 'shall we randomize mercs' ) ):
                        iHuman = gc.getGame().getActivePlayer()
                        lHumanProvinces = self.GMU.getOwnedProvinces( gc.getPlayer(iHuman) )
                        iMercsLeft = 0
                        for lMerc in self.lGlobalPool:
                                #iNewProv = lMercList[lMerc[0]][4][gc.getGame().getSorenRandNum( len(lMercList[lMerc[0]][4]), 'pick available prvonce') ]
                                #if ( ( not ( lMerc[4] in lHumanProvinces ) ) and ( iNewProv in lHumanProvinces ) ):
                                        #CyInterface().addMessage(iHuman, True, con.iDuration/2, CyTranslator().getText("TXT_KEY_MERC_NEW_MERC_AVAILABLE",()), "", 0, "", ColorTypes(con.iLime), -1, -1, True, True)
                                #lMerc[4] = iNewProv
                                if ( gc.getGame().getSorenRandNum( 100, 'mercs leaving the global pool') < lMercList[lMerc[0]][6]/2 ):
                                        self.lGlobalPool.remove( lMerc )
                                        if ( lMerc[4] in lHumanProvinces ):
                                                CyInterface().addMessage(iHuman, True, con.iDuration/2, CyTranslator().getText("TXT_KEY_MERC_NEW_MERC_MOVING",()), "", 0, "", ColorTypes(con.iLime), -1, -1, True, True)
                                        iMercsLeft += 1
                                        if ( iMercsLeft > 1 ):
                                                # don't let too many mercs leave the pool
                                                return
                
        def setPrereqConsistentPromotions( self, lPromotions ):
                bPass = False
                while ( not bPass ):
                        bPass = True
                        for iPromotion in lPromotions:
                                pPromotionInfo = gc.getPromotionInfo( iPromotion )
                                iPrereq = pPromotionInfo.getPrereqOrPromotion1()
                                if ( iPrereq != -1 and ( not iPrereq in lPromotions ) ):
                                        lPromotions.append( iPrereq )
                                        bPass = False
                                iPrereq = pPromotionInfo.getPrereqOrPromotion2()
                                if ( iPrereq != -1 and ( not iPrereq in lPromotions ) ):
                                        lPromotions.append( iPrereq )
                                        bPass = False
                return lPromotions
                
        def addNewMerc( self, iMerc ):
                # this processes the available promotions
                lMercInfo = lMercList[iMerc]
                
                # get the promotions
                iNumPromotions = 0
                lPromotions = []
                iIterations = 0 # limit the number of iterations so we can have mercs with only a few promotions
                while ( iNumPromotions < iNumPromotionsSoftCap and iIterations < iNumPromorionIterations):
                        iPromotion = gc.getGame().getSorenRandNum( iNumTotalPromotions, 'merc get promotion')
                        if ( isPromotionValid(iPromotion, lMercInfo[0], False) ):
                                if ( (not iPromotion in lPromotions) and gc.getGame().getSorenRandNum( 100, 'merc set promotion') < lPromotionOdds[iPromotion] ):
                                        lPromotions.append(iPromotion)
                                        lPromotions = self.setPrereqConsistentPromotions( lPromotions )
                                        iNumPromotions = len( lPromotions )
                        iIterations += 1
                
                (iPurchaseCost, iUpkeepCost) = self.GMU.getCost( iMerc, lPromotions )
                iCurrentProvince = lMercInfo[4][gc.getGame().getSorenRandNum( len(lMercInfo[4]), 'available prvonce') ]
                
                #### DEBUG - start
                #if ( iMerc == 12 or iMerc == 76 ):
                #        iCurrentProvince = xml.iP_Denmark
                #### DEBUG - end
                
                iHuman = gc.getGame().getActivePlayer()
                if ( gc.getPlayer( iHuman ).getProvinceCityCount( iCurrentProvince ) > 0 ):
                        szProvName = "TXT_KEY_PROVINCE_NAME_%i" %iCurrentProvince
                        szCurrentProvince = CyTranslator().getText(szProvName,())
                        CyInterface().addMessage(iHuman, True, con.iDuration/2, CyTranslator().getText("TXT_KEY_MERC_NEW_MERC_AVAILABLE",()) + " " + szCurrentProvince, "", 0, "", ColorTypes(con.iLime), -1, -1, True, True)
                
                # add the merc, keep the merc index, costs and promotions
                self.lGlobalPool.append( [iMerc, lPromotions, iPurchaseCost, iUpkeepCost, iCurrentProvince] )
                #print(" 3Miro Added Merc: ",[iMerc, lPromotions, iPurchaseCost, iUpkeepCost, iCurrentProvince])
                
        def processNewMercs( self, iGameTurn ):
                # add new mercs to the pool
                
                potentialMercs = []
                alreadyAvailableMercs = []
                for iI in range( len( self.lGlobalPool ) ):
                        alreadyAvailableMercs.append( self.lGlobalPool[iI][0] )
                
                for iMerc in range( len( lMercList ) ):
                        if ( self.lHiredBy[iMerc] == -1 and (not iMerc in alreadyAvailableMercs) and iGameTurn >= lMercList[iMerc][2] and iGameTurn <= lMercList[iMerc][3] ):
                                potentialMercs.append( iMerc )
                
                iNumPotentialMercs = len( potentialMercs )
                if ( iNumPotentialMercs == 0 ):
                        return
                # if there are mercs to be potentially added
                iStart = gc.getGame().getSorenRandNum( iNumPotentialMercs, 'starting Merc')
                for iOffset in range( iNumPotentialMercs ):
                        iMerc = potentialMercs[( iOffset + iStart ) % iNumPotentialMercs]
                        if ( gc.getGame().getSorenRandNum( 100, 'merc appearing in global pool') < lMercList[iMerc][6] ):
                                # adding a new merc
                                #print(" 3Miro Adding Merc to Global Pool: ",iMerc)
                                self.addNewMerc( iMerc )
                

        def doMercsTurn( self, iGameTurn ):
        # this is called at the end of the game turn
        # thus the AI gets the advantage to make the Merc "decision" with the most up-to-date political data and they can get the mercs instantly
        # the Human gets the advantage to get the first pick at the available mercs
                #print(" Begin Merc Turn ")
        
                self.getMercLists() # load the current mercenary pool
                iHuman = gc.getGame().getActivePlayer()
                
                #for lMerc in self.lGlobalPool:
                #        print( "3Miro Merc Pool: ", iGameTurn, lMerc)
                
                # Go through each of the players and deduct their mercenary maintenance amount from their gold (round up)
                for iPlayer in range( iNumPlayers - 1 ): # minus the Pope
                        pPlayer = gc.getPlayer( iPlayer )
                        if ( pPlayer.isAlive() ):
                                if ( (pPlayer.getCommercePercent(CommerceTypes.COMMERCE_GOLD) == 100) and (pPlayer.getGold() < (pPlayer.getPicklefreeParameter( iMercCostPerTurn )+99)/100)  ):
                                        # not enough gold to pay the mercs, they will randomly desert you
                                        self.desertMercs( iPlayer )
                                        
                                pPlayer.setGold(pPlayer.getGold()-(pPlayer.getPicklefreeParameter( iMercCostPerTurn )+99)/100 )
                                # TODO: AI
                                if ( iPlayer != iHuman ):
                                        self.processMercAI( pPlayer )
                                        
                        #playerList[i].setGold(playerList[i].getGold()-(playerList[i].getPicklefreeParameter( iMercCostPerTurn )+99)/100 )
                        
                self.rendomizeMercProvinces( iGameTurn ) # some mercs may leave
                
                self.processNewMercs( iGameTurn ) # add new Merc to the pool
                self.processNewMercs( iGameTurn ) # can add up to 2 mercs per turn
                
                ### DEBUG - start
                #self.addNewMerc( 12 )
                #self.addNewMerc( 76 )
                ### DEBUG - end
                
                self.setMercLists() # save the potentially modified merc list (this allows for pickle read/write only once per turn)
                
                #self.GMU.hireMerc( self.lGlobalPool[0], con.iFrankia )
                
                
        def desertMercs( self, iPlayer ):
                pPlayer = gc.getPlayer( iPlayer )
                if ( iPlayer == gc.getGame().getActivePlayer() ):
                        CyInterface().addMessage(gc.getGame().getActivePlayer(), True, con.iDuration/2, CyTranslator().getText("TXT_KEY_MERC_NEW_MERC_DESERTERS",()), "", 0, "", ColorTypes(con.iLightRed), -1, -1, True, True)
                
                bLoop = True
                while ( bLoop ):
                        lHiredMercs = []
                        unitList = PyPlayer( iPlayer ).getUnitList()
                        for pUnit in unitList:
                                if ( pUnit.getMercID() > -1 ):
                                        lHiredMercs.append( pUnit )
                        
                        if ( len( lHiredMercs ) > 0 ):
                                self.GMU.fireMerc( lHiredMercs[ gc.getGame().getSorenRandNum( len( lHiredMercs ), 'deserting Merc') ] )
                                bLoop = ( pPlayer.getGold() < (pPlayer.getPicklefreeParameter( iMercCostPerTurn )+99)/100 )
                        else:
                                # if the player has no mercs, then stop the loop
                                bLoop = False
                                
                        

        def onUnitPromoted( self, argsList ):
                pUnit, iNewPromotion = argsList
                iMerc = pUnit.getMercID()
                if ( iMerc > -1 ):
                        #print(" 3Miro: Unit promoted ",iMerc, pUnit.getOwner() )
                        # redraw the main screen to update the upkeep info
                        CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, True)
                        
                        lPromotionList = []
                        for iPromotion in range(iNumTotalPromotions):
                                if ( pUnit.isHasPromotion( iPromotion ) ):
                                        lPromotionList.append( iPromotion )
                        if ( not iNewPromotion in lPromotionList ):
                                lPromotionList.append( iNewPromotion )
                        
                        # get the new cost for this unit
                        iOwner = pUnit.getOwner()
                        iOldUpkeep = pUnit.getMercUpkeep()
                        dummy, iNewUpkeep = self.GMU.getCost( iMerc, lPromotionList )
                        iNewUpkeep = self.GMU.getModifiedCostPerPlayer( iNewUpkeep, iOwner )
                        
                        pUnit.setMercUpkeep( iNewUpkeep )
                        
                        pPlayer = gc.getPlayer( iOwner )
                        pPlayer.setPicklefreeParameter( iMercCostPerTurn, max( 0, pPlayer.getPicklefreeParameter( iMercCostPerTurn ) - iOldUpkeep + iNewUpkeep  ) )
                        #self.GMU.playerMakeUpkeepSane( iOwner )


        def onUnitKilled(self, argsList):
                pUnit, iAttacker = argsList
                
                iMerc = pUnit.getMercID()
                
                if ( iMerc > -1 ):
                        #print(" 3Miro: Unit killed ",iMerc, pUnit.getOwner() )
                        lHiredByList = self.GMU.getMercHiredBy()
                        if ( lHiredByList[iMerc] == -1 ): # merc was fired, then don't remove permanently
                                return
                        # unit is gone
                        pPlayer = gc.getPlayer( pUnit.getOwner() )
                        pPlayer.setPicklefreeParameter( iMercCostPerTurn, max( 0, pPlayer.getPicklefreeParameter( iMercCostPerTurn ) - pUnit.getMercUpkeep() ) )
                        
                        lHiredByList = self.GMU.getMercHiredBy()
                        # remove the merc permanently
                        lHiredByList[iMerc] = -2
                        self.GMU.setMercHiredBy( lHiredByList )

                

        def onUnitLost(self, argsList):
                # this gets called on lost and on upgrade, check to remove the merc if it has not been upgraded?
                pUnit = argsList[0]
                iMerc = pUnit.getMercID()
                
                if ( iMerc > -1 ):
                        #print(" 3Miro: Unit lost ",iMerc, pUnit.getOwner() )
                        # is a merc, check to see if it has just been killed
                        lHiredByList = self.GMU.getMercHiredBy()
                        if ( lHiredByList[iMerc] < 0 ):
                                # unit has just been killed and onUnitKilled has been called or fired (-1 and -2)
                                return
                        
                        # check to see if it has been replaced by an upgraded (promoted) version of itself
                        # Get the list of units for the player
                        iPlayer = pUnit.getOwner()
                        unitList = PyPlayer( iPlayer ).getUnitList()
                        #for pTestUnit in unitList:
                        #        if ( pTestUnit.getMercID() == iMerc ):
                        #                print("Returning")
                        #                return
                        
                        # unit is gone
                        pPlayer = gc.getPlayer( iPlayer )
                        pPlayer.setPicklefreeParameter( iMercCostPerTurn, max( 0, pPlayer.getPicklefreeParameter( iMercCostPerTurn ) - pUnit.getMercUpkeep() ) )

                        # remove the merc (presumably disbanded here)
                        lHiredByList[iMerc] = -1
                        self.GMU.setMercHiredBy( lHiredByList )

        def processMercAI( self, pPlayer ):
                if ( pPlayer.isHuman() or pPlayer.isBarbarian() or pPlayer.getID() == con.iPope ):
                        return
                        
                #print(" MercAI for ",pPlayer.getID())
                iWarValue = 0 # compute the total number of wars being fought at the moment
                
                teamPlayer = gc.getTeam(pPlayer.getTeam())
                for iOponent in range( con.iNumTotalPlayers ):
                        if ( teamPlayer.isAtWar( gc.getPlayer( iOponent ).getTeam() ) ):
                               iWarValue += 1
                               if ( iOponent <= con.iPope ):
                                       iWarValue += 3
                                       
                # decide to hire or fire mercs
                # if we are at peace or have only a small war, then we can keep the merc if the expense is trivial
                # otherwise we should get rid of some mercs
                # we should also fire mercs if we spend too much
                
                bFire = False
                
                iGold = pPlayer.getGold()
                iUpkeep = pPlayer.getPicklefreeParameter( iMercCostPerTurn )
                
                if ( 100*iGold < iUpkeep ):
                        # can't affort mercs, fire someone
                        bFire = True
                elif ( iWarValue < 4 and 50*iGold < iUpkeep ):
                        # mercs cost > 1/2 of our gold
                        bFire = True
                elif ( iWarValue < 2 and 20*iGold < iUpkeep ):
                        bFire = True
                
                if ( bFire ):
                        # the AI fires a Merc
                        self.FireMercAI( pPlayer )
                        
                        # make sure we can affort the mercs that we keep
                        #print(" Merc Upkeep: ",pPlayer.getPicklefreeParameter( iMercCostPerTurn )," Gold ",pPlayer.getGold() )
                        while ( pPlayer.getPicklefreeParameter( iMercCostPerTurn )>0 and 100*pPlayer.getGold() < pPlayer.getPicklefreeParameter( iMercCostPerTurn ) ):
                                #print(" Merc Upkeep: ",pPlayer.getPicklefreeParameter( iMercCostPerTurn )," Gold ",pPlayer.getGold() )
                                self.GMU.playerMakeUpkeepSane( pPlayer.getID() )
                                self.FireMercAI( pPlayer )
                        return
                        
                if ( iWarValue > 0 ):
                        #we ave to be at war to hire
                        iOdds = con.tHire[pPlayer.getID()]
                        if ( iWarValue < 2 ):
                                iOdds *= 2 # small wars are hardly worth the trouble
                        if ( iWarValue > 4 ): # large war
                                iOdds /= 2
                        
                        if ( gc.getGame().getSorenRandNum(100, 'shall we hire a merc') > iOdds ):
                                # hiring a merc
                                self.HireMercAI( pPlayer )
                        
                        
        def FireMercAI( self, pPlayer ):
                #iNumUnits = pPlayer.getNumUnits()
                lMercs = []
                iGameTurn = gc.getGame().getGameTurn()
                iPlayer = pPlayer.getID()
                unitList = PyPlayer( iPlayer ).getUnitList()
                for pUnit in unitList:
                #for iUnit in range( iNumUnits ):
                        #pUnit = pPlayer.getUnit( iUnit )
                        if ( pUnit.getMercID() > -1 ):
                                lMercs.append( pUnit )
                                
                #print(" Hired Mercs: ",len( lMercs ) )
                                
                if ( len( lMercs ) > 0 ):
                        # we have mercs, so fire someone
                        lMercValue = [] # estimate how "valuable" the merc is (high value is bad)
                        for pUnit in lMercs:
                                iValue = pUnit.getMercUpkeep()
                                pPlot = gc.getMap().plot( pUnit.getX(), pUnit.getY() )
                                if ( pPlot.isCity() ):
                                        if ( pPlot.getPlotCity().getOwner() == pPlayer.getID() ):
                                                # keep the city defenders
                                                iDefenders = self.getNumDefendersAtPlot( pPlot )
                                                if ( iDefenders < 2 ):
                                                        iValue /= 100
                                                elif ( iDefenders < 4 ):
                                                        iValue /= 2
                                
                                if ( iGameTurn > lMercList[ pUnit.getMercID() ][3] ):
                                        # obsolete units
                                        iValue *= 2
                                if ( iGameTurn > lMercList[ pUnit.getMercID() ][3] + 100 ):
                                        # really obsolete units
                                        iValue *= 5
                                lMercValue.append( iValue )
                                
                        iSum = 0
                        for iI in range( len( lMercValue ) ):
                                iSum += lMercValue[iI]

                        iFireRand = gc.getGame().getSorenRandNum(iSum, 'random merc city')
                        for iI in range( len( lMercValue ) ):
                                iFireRand -= lMercValue[iI]
                                if ( iFireRand < 0 ):
                                        self.GMU.fireMerc( lMercs[iI] )
                                        return
                                        
        def HireMercAI( self, pPlayer ):
                # decide which merc to hire
                lCanHireMercs = []
                #sPlayerProvinces = Set( self.getOwnedProvinces( pPlayer ) )
                lPlayerProvinces = self.GMU.getOwnedProvinces( pPlayer )
                iGold = pPlayer.getGold()
                iStateReligion = pPlayer.getStateReligion()
                iPlayer = pPlayer.getID()
                for lMerc in self.lGlobalPool:
                        iMercTotalCost = self.GMU.getModifiedCostPerPlayer( lMerc[2] + (lMerc[3]+99)/100, iPlayer )
                        #sMercProvinces = Set( lMercList[lMerc[0]][4] )
                        #if ( iGold > iMercTotalCost and (not iStateReligion in lMercList[lMerc[0]][5]) and len( sPlayerProvinces & sMercProvinces ) > 0 ):
                        if ( iGold > iMercTotalCost and (not iStateReligion in lMercList[lMerc[0]][5]) and (lMerc[4] in lPlayerProvinces) ):
                              lCanHireMercs.append( lMerc )
                              
                if ( len( lCanHireMercs ) > 0 ):
                        iRandomMerc = gc.getGame().getSorenRandNum(len( lCanHireMercs ), 'random merc to hire')
                        
                        self.GMU.hireMerc( lCanHireMercs[iRandomMerc], pPlayer.getID() )
                        self.getMercLists()
                        
        def getNumDefendersAtPlot( self, pPlot ):
		iOwner = pPlot.getOwner()
		if ( iOwner < 0 ):
			return 0
		iNumUnits = pPlot.getNumUnits()
		iDefenders = 0
		for i in range( iNumUnits ):
			if ( pPlot.getUnit(i).getOwner() == iOwner ):
				iDefenders += 1
		return iDefenders
                
                
class GlobalMercenaryUtils:
        # the idea of this class is to provide ways to manipulate the mercenaries without the need to make a separate instance of the MercenaryManager
        # the MercManager provides event driven functions and those should be called from the event interface
        # the Utils class should be used for interface commands (like for the Human UI)
        
        def getMercGlobalPool( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lMercGlobalPool']
                
        def setMercGlobalPool( self, lNewPool ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lMercGlobalPool'] = lNewPool
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def getMercHiredBy( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lMercsHiredBy']
        
        def setMercHiredBy( self, lNewList ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lMercsHiredBy'] = lNewList
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def getOwnedProvinces( self, pPlayer ):
                lProvList = [] # all available cities that the Merc can appear in
                apCityList = PyPlayer(pPlayer.getID()).getCityList()
                for pCity in apCityList:
                        city = pCity.GetCy()
                        iProvince = city.getProvince()
                        if ( (not (iProvince in lProvList)) and (city.getCultureLevel() >= 2) ):
                              lProvList.append( iProvince )
                return lProvList
                
        def playerMakeUpkeepSane( self, iPlayer ):
                pPlayer = gc.getPlayer( iPlayer )
                unitList = PyPlayer( iPlayer ).getUnitList()
                lMercs = []
                for pUnit in unitList:
                        if ( pUnit.getMercID() > -1 ):
                                lMercs.append( pUnit )
                                
                iTotoalUpkeep = 0
                for pUnit in lMercs:
                        #iTotoalUpkeep += self.getModifiedCostPerPlayer( pUnit.getMercUpkeep(), iPlayer )
                        iTotoalUpkeep += pUnit.getMercUpkeep()
                        
                iSavedUpkeep = pPlayer.getPicklefreeParameter( iMercCostPerTurn )
                if ( iSavedUpkeep != iTotoalUpkeep ):
                        #print(" ERROR IN MERCS: saved upkeep: ",iSavedUpkeep," actual: ",iTotoalUpkeep )
                        #print("  ------- Making sane ------- ")
                        pPlayer.setPicklefreeParameter( iMercCostPerTurn, iTotoalUpkeep )
                        return False
                return True
                
        def getCost( self, iMerc, lPromotions ):
                # note that the upkeep is in the units of 100, i.e. iUpkeepCost = 100 means 1 gold
                lMercInfo = lMercList[iMerc]
                
                # compute cost
                iBaseCost = (80 * gc.getUnitInfo( lMercInfo[0] ).getProductionCost()) / 100
                iPercentage = 0
                for iPromotion in lPromotions:
                        iPercentage += lPromotionCost[iPromotion]
                iPurchaseCost = ( iBaseCost * ( 100 + iPercentage ) ) / 100
                
                # 1 gold of upkeep for 60 hammers cost, minimum 1 gold, maximum 4 gold
                iUpkeepCost = max( 100, min( (100*gc.getUnitInfo( lMercInfo[0] ).getProductionCost())/60, 400 ) )
                iUpkeepCost = iUpkeepCost + 3*iPercentage # 1 gold for 1/3 increase of cost due to promotions
                
                return (iPurchaseCost, iUpkeepCost)
                
        def getModifiedCostPerPlayer( self, iCost, iPlayer ):
                # 3MiroUP: this function gets called:
                #  - every time a merc is hired (pPlayer.initUnit) to set the upkeep and
                #  - every time a merc cost is considered
                #  - every time a merc cost is to be displaded (in the merc screen)
                return ( iCost * lMercCostModifier[iPlayer] ) / 100
                
                
        
        def hireMerc( self, lMerc, iPlayer ):
                # the player would hire a merc
                lGlobalPool = self.getMercGlobalPool()
                lHiredByList = self.getMercHiredBy()
                
                print(" 3Miro: fire Merc: ",lMerc[0], iPlayer )
                
                iCost = self.getModifiedCostPerPlayer( lMerc[2], iPlayer )
                iUpkeep = self.getModifiedCostPerPlayer( lMerc[3], iPlayer )
                
                pPlayer = gc.getPlayer( iPlayer )
                if ( pPlayer.getGold() < iCost ):
                        return
                
                lCityList = [] # all available cities that the Merc can appear in
                apCityList = PyPlayer(iPlayer).getCityList()
                for pCity in apCityList:
                        city = pCity.GetCy()
                        #if ( city.getProvince() in lMercList[ lMerc[0] ][4] ):
                        if ( city.getProvince() == lMerc[4] ):
                              lCityList.append( city )
                              
                if ( len( lCityList ) == 0 ):
                        return
                
                pCity = lCityList[gc.getGame().getSorenRandNum(len(lCityList), 'random merc city')]
                
                iX = pCity.getX()
                iY = pCity.getY()
                
                # do the Gold
                pPlayer.setGold( pPlayer.getGold() - iCost )
                pPlayer.setPicklefreeParameter( iMercCostPerTurn, pPlayer.getPicklefreeParameter( iMercCostPerTurn ) + iUpkeep )
                
                # remove the merc from the golbal pool and set the "hired by" index
                lGlobalPool.remove( lMerc )
                lHiredByList[lMerc[0]] = iPlayer
                
                self.setMercGlobalPool( lGlobalPool )
                self.setMercHiredBy( lHiredByList )
                
                # make the unit:
                pUnit = pPlayer.initUnit( lMercList[lMerc[0]][0], iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH )
                if ( lMercList[lMerc[0]][1] != "TXT_KEY_MERC_GENERIC" ):
                        pUnit.setName( CyTranslator().getText( lMercList[lMerc[0]][1] , ()) )
                
                # add the promotions
                for iPromotion in lMerc[1]:
                        pUnit.setHasPromotion( iPromotion, True )
                        
                pUnit.setHasPromotion( iMercPromotion, True )
                
                # set the MercID
                pUnit.setMercID( lMerc[0] )
                
                # set the Upkeep
                pUnit.setMercUpkeep( iUpkeep )
                
        def fireMerc( self, pMerc ):
                # fires the merc unit pMerc (pointer to CyUnit)
                lHiredByList = self.getMercHiredBy()
                
                # get the Merc info
                iMerc = pMerc.getMercID()
                iUpkeep = pMerc.getMercUpkeep()
                print(" 3Miro: fire Merc: ",iMerc, pMerc.getOwner() )
                
                if ( iMerc < 0 ):
                        return
                
                # free the Merc for a new contract
                lHiredByList[iMerc] = -1
                self.setMercHiredBy( lHiredByList )
                
                # lower the upkeep
                pPlayer = gc.getPlayer( pMerc.getOwner() )
                pPlayer.setPicklefreeParameter( iMercCostPerTurn, max( 0, pPlayer.getPicklefreeParameter( iMercCostPerTurn ) - iUpkeep ) )
                
                pMerc.kill( 0, -1 )
                
                
                
                
                
        
