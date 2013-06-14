#!/usr/bin/python
# -*- coding: latin-1 -*-

import RFCEMaps as maps
import re #for string manipulations

################################################################################################################################################
#
#	Modding script for RFCEurope, written by 3Miro and AbsintheRed
#	Feel free to use it for other mods/purposes (GPLv3 license assumed)
#
#	This script reads RFCEMaps.py (has to be in the same folder), and outputs WB labels
#	Usage:
#		You have to set iOutputType and iPlayer for the desired output
#		Also the part below with the map size (by default the size of RFCEurope)
#		Then call the script:
#			with Unix command (check for permissions): ./Array2WB.py > output_file
#			with Windows command (under cmd): Array2WB.py > output_file.txt
#		The resulted labels have to be copypasted at the end of the WorldBuilder save file
#		The last integer printed is the number of labels, this has to be copied to the "num signs written=" line in BeginMap/EndMap section
#
################################################################################################################################################

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

################################################################################################################################################

#	Edit this part:
#	iOutputType: 1 - WB labels with city names, 2 - WB labels with settler map, 3 - WB labels with war map, 4 - WB labels with province IDs
iOutputType = 1
iPlayer = iHungary

iMapMaxX = 100
iMapMaxY = 73

################################################################################################################################################

def writeCityNames( tMap ):
	iNumSigns = 0
	for iY in range( iMapMaxY ):
		for iX in range( iMapMaxX ):
			if ( tMap[iY][iX] != "-1" ):
				iInvY = iMapMaxY - iY-1
				print "BeginSign\r",
				print "	plotX=%d\r" %iX,
				print "	plotY=%d\r" %iInvY,
				print "	playerType=-1\r",
				print "	caption=%s\r" %tMap[iY][iX],
				print "EndSign\r",
				iNumSigns += 1
	print iNumSigns

def writeSettlersMap( tMap ):
	iNumSigns = 0
	for iY in range( iMapMaxY ):
		for iX in range( iMapMaxX ):
			if ( tMap[iY][iX] != 20 ):
				iInvY = iMapMaxY - iY-1
				print "BeginSign\r",
				print "	plotX=%d\r" %iX,
				print "	plotY=%d\r" %iInvY,
				print "	playerType=-1\r",
				print "	caption=%d\r" %tMap[iY][iX],
				print "EndSign\r",
				iNumSigns += 1
	print iNumSigns

def writeWarMap( tMap ):
	iNumSigns = 0
	for iY in range( iMapMaxY ):
		for iX in range( iMapMaxX ):
			if ( tMap[iY][iX] != 0 ):
				iInvY = iMapMaxY - iY-1
				print "BeginSign\r",
				print "	plotX=%d\r" %iX,
				print "	plotY=%d\r" %iInvY,
				print "	playerType=-1\r",
				print "	caption=%d\r" %tMap[iY][iX],
				print "EndSign\r",
				iNumSigns += 1
	print iNumSigns

def writeProvinceMap( tMap ):
	iNumSigns = 0
	for iY in range( iMapMaxY ):
		for iX in range( iMapMaxX ):
			if ( tMap[iY][iX] != -1 ):
				iInvY = iMapMaxY - iY-1
				print "BeginSign\r",
				print "	plotX=%d\r" %iX,
				print "	plotY=%d\r" %iInvY,
				print "	playerType=-1\r",
				print "	caption=%d\r" %tMap[iY][iX],
				print "EndSign\r",
				iNumSigns += 1
	print iNumSigns


if ( iOutputType == 1 ):
	writeCityNames( maps.tCityMap[iPlayer] )
elif ( iOutputType == 2 ):
	writeSettlersMap( maps.tSettlersMaps[iPlayer] )
elif ( iOutputType == 3 ):
	writeWarMap( maps.tWarsMaps[iPlayer] )
elif ( iOutputType == 4 ):
	writeProvinceMap( maps.tProinceMap )
