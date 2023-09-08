# DLL Data Loader for RFC Europe
# Implemented by AbsintheRed, based on SoI

from CvPythonExtensions import *
import RFCEMaps as maps
import Consts

gc = CyGlobalContext()


def setup():
    """Loads the data from RFCEMaps.py into appropriate objects within CvGameCoreDLL."""

    # Region (province) maps
    map = CyMap()
    for y in range(len(maps.tProvinceMap)):
        for x in range(len(maps.tProvinceMap[y])):
            plot = map.plot(
                x, y
            )  # no need for [iMaxY - iY - 1] inversion, the province map is upside down visually
            if plot:
                plot.setProvinceID(maps.tProvinceMap[y][x])
                # print ('ProvinceID', x, y, plot.getProvinceID)

    # City name maps
    for iLoopPlayer in range(
        Consts.iNumPlayers - 1
    ):  # currently neither the papal nor the default maps are added
        if len(maps.tCityMap) > iLoopPlayer:
            for y in range(len(maps.tCityMap[iLoopPlayer])):
                for x in range(len(maps.tCityMap[iLoopPlayer][y])):
                    plot = map.plot(
                        x, len(maps.tCityMap[iLoopPlayer]) - 1 - y
                    )  # because Civ4 maps are reversed on Y-axis
                    if plot:
                        sName = maps.tCityMap[iLoopPlayer][y][x]
                        # Set the value in CvPlot instance
                        plot.setCityNameMap(iLoopPlayer, sName)

    # Lake name IDs
    # first set all plots to -1
    for y in range(len(maps.tProvinceMap)):
        for x in range(len(maps.tProvinceMap[y])):
            plot = map.plot(x, y)
            if plot:
                plot.setLakeNameID(-1)
    # then we add the ID to the actual lake tiles
    for i in range(len(Consts.lLakeNameIDs)):
        x = Consts.lLakeNameIDs[i][0]
        y = Consts.lLakeNameIDs[i][1]
        iLakeNameID = Consts.lLakeNameIDs[i][2]
        plot = map.plot(x, y)
        if plot:
            plot.setLakeNameID(iLakeNameID)
