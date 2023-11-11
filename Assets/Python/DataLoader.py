# DLL Data Loader for RFC Europe
# Implemented by AbsintheRed, based on SoI

from CvPythonExtensions import *
from MapsData import CITIES_MAP, PROVINCES_MAP
from CoreData import civilizations
from LocationsData import LAKE_LOCATIONS

gc = CyGlobalContext()


def setup():
    """Loads the data from RFCEMaps.py into appropriate objects within CvGameCoreDLL."""

    # Region (province) maps
    map = CyMap()
    for y in range(len(PROVINCES_MAP)):
        for x in range(len(PROVINCES_MAP[y])):
            plot = map.plot(
                x, y
            )  # no need for [iMaxY - iY - 1] inversion, the province map is upside down visually
            if plot:
                plot.setProvinceID(PROVINCES_MAP[y][x])

    # City name maps
    for civ in (
        civilizations().main().ids()
    ):  # currently neither the papal nor the default maps are added
        if len(CITIES_MAP) > civ:
            for y in range(len(CITIES_MAP[civ])):
                for x in range(len(CITIES_MAP[civ][y])):
                    plot = map.plot(
                        x, len(CITIES_MAP[civ]) - 1 - y
                    )  # because Civ4 maps are reversed on Y-axis
                    if plot:
                        sName = CITIES_MAP[civ][y][x]
                        # Set the value in CvPlot instance
                        plot.setCityNameMap(civ, sName)

    # Lake name IDs
    # first set all plots to -1
    for y in range(len(PROVINCES_MAP)):
        for x in range(len(PROVINCES_MAP[y])):
            plot = map.plot(x, y)
            if plot:
                plot.setLakeNameID(-1)
    # then we add the ID to the actual lake tiles
    for name, locations in LAKE_LOCATIONS.items():
        for location in locations:
            plot = map.plot(*location.to_tuple())
            if plot:
                plot.setLakeNameID(name.value)
