#!/usr/bin/python

#import Consts as con

import RFCEMaps as maps

import re #for string manipulations

################################################################################################################################################
#   Moding script for RFCEurope, written by 3Miro, feel free to use it for other mods/purposes (assume license GPLv3)
#       
#   This script reads RFCEMaps.py (in the same folder) and outputs WB labels
#   Set iOutputType and iPlayer for the desired output
#   The resulting labels have to be copy/pasted at the end of the WorldBuilder save file
#   The last integer printed is the number of labels, this has to be copied over xxx in "num signs written=xxx" in BeginMap/EndMap section
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


######################################################################
##### Edit this Part ################

#iOutputType = 2 # 1 - WB labels with city names, 2 - WB labels with Settlers Map, 3 - WB labels with War maps
iOutputType = 1

iPlayer = iGermany

iMapMaxX = 100
iMapMaxY = 73


######################################################################





def populate_array(rows, columns):
        #array_dic = {}
        #for row in range(1, rows+1):     ## starts with one, not zero
        #        array_dic[row] = []
        #        for col in range(0, columns):
        #                array_dic[row].append('None')     ## initialize to 'None'
        return [[0 for i in range(columns)] for j in range(rows)]
        
def write_array_to_Javascript(rows, columns, array ):
        #f = open('JavascriptArray.txt', 'w')
        for iY in range( iMapMaxY ):
                for iX in range( iMapMaxX ):
                        #sstr = ( "\"%d\"," %array[iY][iX] )
                        sstr = ( "%d," %array[iY][iX] )
                        print sstr,

def write_array_to_Python(rows, columns, array ):
        #f = open('JavascriptArray.txt', 'w')
        for iY in range( iMapMaxY ):
                print "(",
                for iX in range( iMapMaxX ):
                        #sstr = ( "\"%d\"," %array[iY][iX] )
                        if ( iX < iMapMaxX -1 ):
                                sstr = ( "%d," %array[iY][iX] )
                        else:
                                sstr = ( "%d" %array[iY][iX] )
                        print sstr,
                print "),"

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


if ( iOutputType == 1 ):
	writeCityNames( maps.tCityMap[iPlayer] )
elif ( iOutputType == 2 ):
        writeSettlersMap( maps.tSettlersMaps[iPlayer] )
elif ( iOutputType == 3 ):
        writeWarMap( maps.tWarsMaps[iPlayer] )
