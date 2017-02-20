# DLL Data Loader for RFC Europe
# Implemented by AbsintheRed, based on SoI

from CvPythonExtensions import *
import RFCEMaps as maps

gc = CyGlobalContext()

def setup():
	"""Loads the data from RFCEMaps.py into appropriate objects within CvGameCoreDLL."""

	# Region (province) maps
	map = CyMap()
	for y in range(len(maps.tProinceMap)):
		for x in range(len(maps.tProinceMap[y])):
			plot = map.plot(x, y) # no need for [iMaxY - iY - 1] inversion, the province map is upside down visually
			if plot:
				plot.setProvinceID(maps.tProinceMap[y][x])
				print ('ProvinceID', x, y, plot.getProvinceID)

