# Rhye's and Fall of Civilization: Europe - City naming and renaming management

from CvPythonExtensions import *
import PyHelpers
import Consts as con
import RFCEMaps as rfcemaps

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

# city coordinates
tCityMap = rfcemaps.tCityMap


class CityNameManager:
    def assignName(self, city):
        """Names a city depending on its plot"""
        iOwner = city.getOwner()
        if iOwner < con.iNumMajorPlayers:
            # print(" City Name ",iOwner,con.iMapMaxY-1-city.getY(),city.getX()) #Sedna17 Needed to throw an extra -1 in the Y coordinate to get things to line up right. I love zero-indexing.
            cityName = tCityMap[iOwner][con.iMapMaxY - 1 - city.getY()][city.getX()]
            # print(" City Name ",cityName)
            if cityName != "-1":
                city.setName(unicode(cityName, "latin-1"), False)

    def renameCities(self, city, iNewOwner):
        """Renames a city depending on its owner"""

        # sName = city.getName()
        if iNewOwner < con.iNumMajorPlayers:
            cityName = tCityMap[iNewOwner][con.iMapMaxY - 1 - city.getY()][city.getX()]
            if cityName != "-1":
                city.setName(unicode(cityName, "latin-1"), False)

    def lookupName(self, city, iPlayer):
        """Looks up a city name in another player's map"""
        if iPlayer < con.iNumMajorPlayers:
            cityName = tCityMap[iPlayer][con.iMapMaxY - 1 - city.getY()][city.getX()]
            if cityName == "-1":
                return "Unknown"
            else:
                return cityName
