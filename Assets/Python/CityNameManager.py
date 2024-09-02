# Rhye's and Fall of Civilization: Europe - City naming and renaming management

from CvPythonExtensions import *
from Core import civilizations, get_data_from_upside_down_map
from CityMapData import CITIES_MAP
from Events import handler

gc = CyGlobalContext()


@handler("cityBuilt")
def onCityBuilt(city):
    assignName(city)


@handler("cityAcquired")
def onCityAcquired(iOwner, iNewOwner, city):
    renameCities(city, iNewOwner)


def assignName(city):
    """Names a city depending on its plot"""
    iOwner = city.getOwner()
    if iOwner < civilizations().majors().len():
        cityName = get_data_from_upside_down_map(CITIES_MAP, iOwner, city)
        if cityName != "-1":
            city.setName(unicode(cityName), False)


def renameCities(city, iNewOwner):
    """Renames a city depending on its owner"""
    if iNewOwner < civilizations().majors().len():
        cityName = get_data_from_upside_down_map(CITIES_MAP, iNewOwner, city)
        if cityName != "-1":
            city.setName(unicode(cityName), False)


def lookupName(city, iPlayer):
    """Looks up a city name in another player's map"""
    if iPlayer < civilizations().majors().len():
        cityName = get_data_from_upside_down_map(CITIES_MAP, iPlayer, city)
        if cityName == "-1":
            return "Unknown"
        else:
            return cityName
