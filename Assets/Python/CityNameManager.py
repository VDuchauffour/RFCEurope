# Rhye's and Fall of Civilization: Europe - City naming and renaming management

from CvPythonExtensions import *
from CoreData import CIVILIZATIONS
import PyHelpers
import RFCEMaps
from MiscData import WORLD_HEIGHT

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer


class CityNameManager:
    def assignName(self, city):
        """Names a city depending on its plot"""
        iOwner = city.getOwner()
        if iOwner < CIVILIZATIONS.majors().len():
            cityName = RFCEMaps.tCityMap[iOwner][WORLD_HEIGHT - 1 - city.getY()][city.getX()]
            if cityName != "-1":
                city.setName(unicode(cityName, "latin-1"), False)

    def renameCities(self, city, iNewOwner):
        """Renames a city depending on its owner"""

        # sName = city.getName()
        if iNewOwner < CIVILIZATIONS.majors().len():
            cityName = RFCEMaps.tCityMap[iNewOwner][WORLD_HEIGHT - 1 - city.getY()][city.getX()]
            if cityName != "-1":
                city.setName(unicode(cityName, "latin-1"), False)

    def lookupName(self, city, iPlayer):
        """Looks up a city name in another player's map"""
        if iPlayer < CIVILIZATIONS.majors().len():
            cityName = RFCEMaps.tCityMap[iPlayer][WORLD_HEIGHT - 1 - city.getY()][city.getX()]
            if cityName == "-1":
                return "Unknown"
            else:
                return cityName
