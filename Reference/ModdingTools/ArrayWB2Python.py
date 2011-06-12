#!/usr/bin/python

#import Consts as con

import re #for string manipulations

################################################################################################################################################
#   Moding script for RFCEurope, written by 3Miro, feel free to use it for other mods/purposes (assume license GPLv3)
#       
#       This Script reads a WorldBuilder file into three types of arrays
#       
#       Python Array:   
#			for Settlers Map and War Map
#			assumes the map contains a bunch of labels with ONLY NUMBERS, then it reads those and outputs
#                       generates output of a Python array that can be places in RFCEMaps.py
#
#       City Name Map:
#			writes the labels into an array of strings
#
#	You need to edit tWBFilename and iOutputType
#
#       Usage:
#               edit the part below with the map size (by default the size of RFCEurope) and file-name of the WB file
#               then call the script with Unix command (check for permissions)
#                       ./Province2WBArray.py > output_file
#               or Windows command
#                       Province2WBArray.py > output_file.txt
#
#               Get the output Arrays from output_file.txt, you can copy/paste that in either RFCEMaps.py or the HTML file
#
################################################################################################################################################


######################################################################
##### Edit this Part ################

#tWBFilename = "LithuaniaWarsMap.CivBeyondSwordWBSave"
#tWBFilename = "LithuaniaSettlersMap.CivBeyondSwordWBSave"
#tWBFilename = "PolandWarsMap.CivBeyondSwordWBSave"
#tWBFilename = "PolandSettlersMap.CivBeyondSwordWBSave"
#tWBFilename = "PortugalWarsMap.CivBeyondSwordWBSave"
#tWBFilename = "CordobaSettlersMap.CivBeyondSwordWBSave"
#tWBFilename = "PortugalSettlersMap.CivBeyondSwordWBSave"
#tWBFilename = "PolandNewCityNamesAndResources.CivBeyondSwordWBSave"
tWBFilename = "SwedenCityNames.CivBeyondSwordWBSave"

iOutputType = 3 # 1 - Settlers Map 2 Array, 2 - War Map 2 Array. 3 - City Name Map


iMapMaxX = 100
iMapMaxY = 73


######################################################################

iOcean = 0
iDesert = 1
iPlains = 2
iGrass = 3
iCoast = 4
iMoor = 5
iTundra = 6
iMarsh = 7
iMountain = 8 # PlotType = 0


def populate_array(rows, columns):
        #array_dic = {}
        #for row in range(1, rows+1):     ## starts with one, not zero
        #        array_dic[row] = []
        #        for col in range(0, columns):
        #                array_dic[row].append('None')     ## initialize to 'None'
        return [[0 for i in range(columns)] for j in range(rows)]

def populate_array_string(rows, columns):
        #array_dic = {}
        #for row in range(1, rows+1):     ## starts with one, not zero
        #        array_dic[row] = []
        #        for col in range(0, columns):
        #                array_dic[row].append('None')     ## initialize to 'None'
        return [["-1" for i in range(columns)] for j in range(rows)]
        
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
                                sstr = ( "%d," %array[iMapMaxY-iY-1][iX] )
                        else:
                                sstr = ( "%d" %array[iMapMaxY-iY-1][iX] )
                        print sstr,
                print "),"

def write_array_to_PythonCity(rows, columns, array ):
        #f = open('JavascriptArray.txt', 'w')
        for iY in range( iMapMaxY ):
                print "(",
                for iX in range( iMapMaxX ):
                        #sstr = ( "\"%d\"," %array[iY][iX] )
			#if ( array[iMapMaxY-iY-1][iX] == "-1" ):
	                #       if ( iX < iMapMaxX -1 ):
        	        #                sstr = ( "\"%d\"," %array[iMapMaxY-iY-1][iX] )
                	#        else:
                        #	        sstr = ( "\"%d\"" %array[iMapMaxY-iY-1][iX] )
			#else:
			#	if ( iX < iMapMaxX -1 ):
        	        #                sstr = ( "\"%s\"," %array[iMapMaxY-iY-1][iX] )
                	#        else:
                        #	        sstr = ( "\"%s\"" %array[iMapMaxY-iY-1][iX] )
                        if ( iX < iMapMaxX -1 ):
        	                sstr = ( "\"%s\"," %array[iMapMaxY-iY-1][iX] )
                	else:
                                sstr = ( "\"%s\"" %array[iMapMaxY-iY-1][iX] )
                        print sstr,
                print "),"

def findCapital(rows, columns, array ):
        #f = open('JavascriptArray.txt', 'w')
        for iY in range( iMapMaxY ):
                for iX in range( iMapMaxX ):
			if ( array[iY][iX] == 700 ):
				print iX, iY

def parseLabels2ArraySettler():
        tProv = populate_array( iMapMaxY, iMapMaxX )
        for iY in range( iMapMaxY ):
                for iX in range( iMapMaxX ):
                        tProv[iY][iX] = 20
        f = open(tWBFilename, "r")
        bSignStart = False
        bWaitTerrain = False
        bMountNotSet = False
        iCount = 0
        iX = 0
        iY = 0
        iV = 0
        for line in f:
                line = line.strip("\n").strip("\r")
                if ( (not bSignStart) and "### Sign Info ###" ):
                        bSignStart = True
                if ( "plotX=" in line ):
                        iX = int( line.strip("	plotX=") )
                if ( "plotY=" in line ):
                        iY = int( line.strip("	plotY=") )
                if ( "caption=" in line ):
                        tProv[iY][iX] = int( line.strip("	caption=") )

        write_array_to_Python( iMapMaxY, iMapMaxX, tProv )
	#findCapital( iMapMaxY, iMapMaxX, tProv )

def parseLabels2ArrayWar():
        tProv = populate_array( iMapMaxY, iMapMaxX )
        for iY in range( iMapMaxY ):
                for iX in range( iMapMaxX ):
                        tProv[iY][iX] = 0
        f = open(tWBFilename, "r")
        bSignStart = False
        bWaitTerrain = False
        bMountNotSet = False
        iCount = 0
        iX = 0
        iY = 0
        iV = 0
        for line in f:
                line = line.strip("\n").strip("\r")
                if ( (not bSignStart) and "### Sign Info ###" ):
                        bSignStart = True
                if ( "plotX=" in line ):
                        iX = int( line.strip("	plotX=") )
                if ( "plotY=" in line ):
                        iY = int( line.strip("	plotY=") )
                if ( "caption=" in line ):
                        tProv[iY][iX] = int( line.strip("	caption=") )

        write_array_to_Python( iMapMaxY, iMapMaxX, tProv )

def parseLabels2ArrayCity():
        tProv = populate_array_string( iMapMaxY, iMapMaxX )
        f = open(tWBFilename, "r")
        bSignStart = False
        bWaitTerrain = False
        bMountNotSet = False
        iCount = 0
        iX = 0
        iY = 0
        iV = 0
        for line in f:
                line = line.strip("\n").strip("\r")
                if ( (not bSignStart) and "### Sign Info ###" ):
                        bSignStart = True
                if ( "plotX=" in line ):
                        iX = int( line.strip("	plotX=") )
                if ( "plotY=" in line ):
                        iY = int( line.strip("	plotY=") )
                if ( "caption=" in line ):
                        #if ( iY == 49 and iX == 65 ):
                        #        print line
                        #        print line[10]
                        #        print line[11]
                        #        print line[12]
                        #        print line[13]
                        #       print line[14]
                        #tProv[iY][iX] = line.strip("	caption=")
                        tProv[iY][iX] = line[9:]
                        #tProv[iY][iX] = line[12]
                        #if ( iY == 49 and iX == 65 ):
                        #        print tProv[iY][iX]

        #print tProv[49][65]

        write_array_to_PythonCity( iMapMaxY, iMapMaxX, tProv )

if ( iOutputType == 1 ):
        parseLabels2ArraySettler()
elif ( iOutputType == 2 ):
        parseLabels2ArrayWar()
else:
	parseLabels2ArrayCity()
