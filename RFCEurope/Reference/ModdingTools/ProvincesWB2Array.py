#!/usr/bin/python

import re #for string manipulations

################################################################################################################################################
#
#	Modding script for RFCEurope, written by 3Miro and AbsintheRed
#	Feel free to use it for other mods/purposes (GPLv3 license assumed)
#
#	This Script reads a WorldBuilder file, and writes it into three types of arrays:
#		Javascript array of the map:
#			Generates a Javascript array in row major format with numbers depending on the terrain type
#			You can use that for visualization purposes in the HTML file
#		Javascript array of provinces:
#			Assumes the map contains a bunch of labels with ONLY NUMBERS
#			Outputs a Javascript array that can be used to visualize Provinces in the HTML file
#		Python array of provinces:
#			Assumes the map contains a bunch of labels with ONLY NUMBERS
#			Generates output of a Python array that can be placed in the province section of RFCEMaps.py
#
#	Usage:
#		You need to set iOutputType and the tWBFilename (file-name of the WB file)
#		Also the part below with the map size (by default the size of RFCEurope)
#		Then call the script:
#			with Unix command (check for permissions): ./ProvincesWB2Array.py > output_file
#			with Windows command (under cmd): ProvincesWB2Array.py > output_file.txt
#		Get the output arrays from output_file.txt, and you can copypaste it into either RFCEMaps.py or the HTML file
#
################################################################################################################################################

#	Edit this part:
#	iOutputType: 1 - Javascript array of the map, 2 - Javascript array of provinces, 3 - Python array of provinces
iOutputType = 3
tWBFilename = "Provinces.CivBeyondSwordWBSave"

iMapMaxX = 100
iMapMaxY = 73

################################################################################################################################################

iOcean = 0
iDesert = 1
iPlains = 2
iGrass = 3
iCoast = 4
iMoor = 5
iTundra = 6
iMarsh = 7
iMountain = 8	#PlotType=0

def populate_array(rows, columns):
#	array_dic = {}
#	for row in range(1, rows+1):		## starts with one, not zero
#		array_dic[row] = []
#		for col in range(0, columns):
#			array_dic[row].append('None')		## initialize to 'None'
	return [[0 for i in range(columns)] for j in range(rows)]

def write_array_to_Javascript(rows, columns, array ):
	for iY in range( iMapMaxY ):
		for iX in range( iMapMaxX ):
			sstr = ( "%d," %array[iY][iX] )
			print sstr,

def write_array_to_Python(rows, columns, array ):
	for iY in range( iMapMaxY ):
		print "(",
		for iX in range( iMapMaxX ):
			if ( iX < iMapMaxX -1 ):
				sstr = ( "%d," %array[iY][iX] )
			else:
				sstr = ( "%d" %array[iY][iX] )
			print sstr,
		print "),"

def parseTerrain():
	tProv = populate_array( iMapMaxY, iMapMaxX )
	for iY in range( iMapMaxY ):
		for iX in range( iMapMaxX ):
			tProv[iY][iX] = 0
	f = open(tWBFilename, 'r')
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
	write_array_to_Javascript( iMapMaxY, iMapMaxX, tProv )

def parseProvinces2Javascript():
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
	write_array_to_Javascript( iMapMaxY, iMapMaxX, tProv )

def parseProvinces2Python():
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
	write_array_to_Python( iMapMaxY, iMapMaxX, tProv )


if ( iOutputType == 1 ):
	parseTerrain()
elif ( iOutputType == 2 ):
	parseProvinces2Javascript()
elif ( iOutputType == 3 ):
	parseProvinces2Python()
