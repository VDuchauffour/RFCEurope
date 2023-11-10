# Rhye's and Fall of Civilization: Europe - City naming and renaming management

from CvPythonExtensions import *
from CoreData import civilizations
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
        if iOwner < civilizations().majors().len():
            cityName = RFCEMaps.CITIES_MAP[iOwner][WORLD_HEIGHT - 1 - city.getY()][city.getX()]
            if cityName != "-1":
                city.setName(unicode(cityName, "latin-1"), False)  # type: ignore

    def renameCities(self, city, iNewOwner):
        """Renames a city depending on its owner"""

        # sName = city.getName()
        if iNewOwner < civilizations().majors().len():
            cityName = RFCEMaps.CITIES_MAP[iNewOwner][WORLD_HEIGHT - 1 - city.getY()][city.getX()]
            if cityName != "-1":
                city.setName(unicode(cityName, "latin-1"), False)  # type: ignore

    def lookupName(self, city, iPlayer):
        """Looks up a city name in another player's map"""
        if iPlayer < civilizations().majors().len():
            cityName = RFCEMaps.CITIES_MAP[iPlayer][WORLD_HEIGHT - 1 - city.getY()][city.getX()]
            if cityName == "-1":
                return "Unknown"
            else:
                return cityName
