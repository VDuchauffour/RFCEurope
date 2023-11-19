# Rhye's and Fall of Civilization: Europe - City naming and renaming management

from CvPythonExtensions import *
from CoreData import civilizations
from CityMapData import CITIES_MAP
from CoreFunctions import get_civ_by_id
from MiscData import WORLD_HEIGHT

gc = CyGlobalContext()


class CityNameManager:
    def assignName(self, city):
        """Names a city depending on its plot"""
        iOwner = city.getOwner()
        if iOwner < civilizations().majors().len():
            cityName = CITIES_MAP[get_civ_by_id(iOwner)][WORLD_HEIGHT - 1 - city.getY()][
                city.getX()
            ]
            if cityName != "-1":
                city.setName(unicode(cityName, "latin-1"), False)  # type: ignore

    def renameCities(self, city, iNewOwner):
        """Renames a city depending on its owner"""
        if iNewOwner < civilizations().majors().len():
            cityName = CITIES_MAP[get_civ_by_id(iNewOwner)][WORLD_HEIGHT - 1 - city.getY()][
                city.getX()
            ]
            if cityName != "-1":
                city.setName(unicode(cityName, "latin-1"), False)  # type: ignore

    def lookupName(self, city, iPlayer):
        """Looks up a city name in another player's map"""
        if iPlayer < civilizations().majors().len():
            cityName = CITIES_MAP[get_civ_by_id(iPlayer)][WORLD_HEIGHT - 1 - city.getY()][
                city.getX()
            ]
            if cityName == "-1":
                return "Unknown"
            else:
                return cityName
