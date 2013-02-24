#!/usr/bin/python

import re #for string manipulations

################################################################################################################################################
#
#	Modding script for RFCEurope, written by 3Miro and AbsintheRed
#	Feel free to use it for other mods/purposes (GPLv3 license assumed)
#
#	This Script reads a WorldBuilder file, and writes it into three types of arrays:
#		Settler Maps and War Maps into a Python array:
#			Assumes the map contains a bunch of labels with ONLY NUMBERS
#			Generates output of a Python array that can be placed in the RFCEMaps.py
#		City Name Maps into an array of strings:
#			Writes the labels into an array of strings
#
#	Usage:
#		You need to set iOutputType and the tWBFilename (file-name of the WB file)
#		Also the part below with the map size (by default the size of RFCEurope)
#		Then call the script:
#			with Unix command (check for permissions): ./ArrayWB2Python.py > output_file
#			with Windows command (under cmd): ArrayWB2Python.py > output_file.txt
#		Get the output arrays from output_file.txt, and you can copypaste it into the corresponding parts of RFCEMaps.py
#
################################################################################################################################################

#	Edit this part:
#	iOutputType: 1 - Settler Map to array, 2 - War Map to array, 3 - City Name Map to array
iOutputType = 3
tWBFilename = "Hungary.CivBeyondSwordWBSave"

iMapMaxX = 100
iMapMaxY = 73

################################################################################################################################################

def populate_array(rows, columns):
#	array_dic = {}
#	for row in range(1, rows+1):		## starts with one, not zero
#		array_dic[row] = []
#		for col in range(0, columns):
#			array_dic[row].append('None')		## initialize to 'None'
	return [[0 for i in range(columns)] for j in range(rows)]

def populate_array_string(rows, columns):
#	array_dic = {}
#	for row in range(1, rows+1):		## starts with one, not zero
#		array_dic[row] = []
#		for col in range(0, columns):
#			array_dic[row].append('None')		## initialize to 'None'
	return [["-1" for i in range(columns)] for j in range(rows)]

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

def write_array_to_PythonCity(rows, columns, array ):
	for iY in range( iMapMaxY ):
		print "(",
		for iX in range( iMapMaxX ):
			if ( iX < iMapMaxX -1 ):
				sstr = ("\"%s\"," %array[iMapMaxY-iY-1][iX])
			else:
				sstr = ("\"%s\"" %array[iMapMaxY-iY-1][iX])
			print sstr,
		print "),"

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
			#tProv[iY][iX] = line.strip("	caption=")
			tProv[iY][iX] = line[9:]
	write_array_to_PythonCity( iMapMaxY, iMapMaxX, tProv )


if ( iOutputType == 1 ):
	parseLabels2ArraySettler()
elif ( iOutputType == 2 ):
	parseLabels2ArrayWar()
elif ( iOutputType == 3 ):
	parseLabels2ArrayCity()
