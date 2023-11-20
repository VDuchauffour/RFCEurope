# DLL Data Loader for RFC Europe
# Implemented by AbsintheRed, based on SoI

from CvPythonExtensions import *
from CityMapData import CITIES_MAP
from ProvinceMapData import PROVINCES_MAP
from CoreData import civilizations
from LocationsData import LAKE_LOCATIONS

gc = CyGlobalContext()


def setup():
    """Loads the data from RFCEMaps.py into appropriate objects within CvGameCoreDLL."""

    # Region (province) maps
    map = CyMap()
    for y in range(len(PROVINCES_MAP)):
        for x in range(len(PROVINCES_MAP[y])):
            plot = map.plot(x, y)
            if plot:
                plot.setProvinceID(PROVINCES_MAP[y][x])

    # City name maps
    # currently neither the papal nor the default maps are added
    for civ in civilizations().main():
        for y, row in enumerate(CITIES_MAP[civ.key]):
            for x, cell in enumerate(row):
                plot = map.plot(x, len(CITIES_MAP[civ.key]) - 1 - y)
                if plot:
                    plot.setCityNameMap(civ.id, cell)

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
