#!/usr/bin/python

#import Consts as con

import re #for string manipulations

################################################################################################################################################
#   Moding script for RFCEurope, written by 3Miro, feel free to use it for other mods/purposes (assume license GPLv3)
#       
#       This Script reads a WorldBuilder file into three types of arrays
#       Javascript Map: generates a Javascript array in row major format with numvers depending on the terrain type
#                       you can use that to place for visualization purposes in the HTML file
#       Javascript Provinces:   assumes the map contains a bunch of labels with ONLY NUMBERS, then it reads those and outputs
#                               a Javascript array that can be used to visualize Provinces in the HTML file
#       Python Array:   assumes the map contains a bunch of labels with ONLY NUMBERS, then it reads those and outputs
#                       generates output of a Python array that can be placed in RFCEMaps.py
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

tWBFilename = "Provinces.CivBeyondSwordWBSave"
iOutputType = 3 # 1 - Javascript Province, 2 - Javascript Map, 3 - Python Array for Maps.py

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


def parseProvinces2Javascript( iTypeOfOutput ):
        tProv = populate_array( iMapMaxY, iMapMaxX )
        for iY in range( iMapMaxY ):
                for iX in range( iMapMaxX ):
                        tProv[iY][iX] = -1
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

        if ( iTypeOfOutput == 1 ):
                write_array_to_Javascript( iMapMaxY, iMapMaxX, tProv )
        else:
                write_array_to_Python( iMapMaxY, iMapMaxX, tProv )

def parseTerrain():
        tProv = populate_array( iMapMaxY, iMapMaxX )
        for iY in range( iMapMaxY ):
                for iX in range( iMapMaxX ):
                        tProv[iY][iX] = 0
        f = open('Test.CivBeyondSwordWBSave', 'r')
        bWaitTerrain = False
        bMountNotSet = False
        iCount = 0
        iX = 0
        iY = 0
        iV = 0
        for line in f:
                line = line.strip("\n").strip("\r")
                if ( "PlotType=0" in line ):
                      tProv[iY][iX] = iMountain
                      bMountNotSet = False
                      bWaitTerrain = False
                if ( bWaitTerrain and bMountNotSet ):
                        if ( "TerrainType" in line ):
                                bWaitTerrain = False
                                if ( "TERRAIN_OCEAN" in line ):
                                        iV = iOcean
                                if ( "TERRAIN_DESERT" in line ):
                                        iV = iDesert
                                if ( "TERRAIN_PLAINS" in line ):
                                        iV = iPlains
                                if ( "TERRAIN_GRASS" in line ):
                                        iV = iGrass
                                if ( "TERRAIN_MOORLAND" in line ):
                                        iV = iMoor
                                if ( "TERRAIN_TUNDRA" in line ):
                                        iV = iTundra
                                if ( "TERRAIN_MARSH" in line ):
                                        iV = iMarsh
                                if ( "TERRAIN_COAST" in line ):
                                        iV = iCoast
                                tProv[iY][iX] = iV
                else:
                        if ( ",y=" in line ):
                                bWaitTerrain = True
                                bMountNotSet = True
                                tmp = re.split('[,]+', line)
                                iX = int( tmp[0].strip("	x=") )
                                iY = int( tmp[1].strip("y=") )
                                #print( [iX,iY], "\n" )

        write_array_to_Javascript( iMapMaxY, iMapMaxX, tProv )

if ( iOutputType == 2 ):
        parseTerrain()
else:
        parseProvinces2Javascript(iOutputType)
