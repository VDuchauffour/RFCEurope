from CvPythonExtensions import CyGlobalContext
from CityNameManager import renameCities
from Core import civilizations, get_scenario, cities
from CoreTypes import Civ, Scenario
from PyUtils import rand
from StoredData import data
from Events import handler

gc = CyGlobalContext()


@handler("GameStart")
def setup():
    reset_stored_data()
    misc()


def reset_stored_data():
    data.setup()


def misc():
    # Absinthe: Turn Randomization constants
    iLighthouseEarthQuake = 0
    iByzantiumVikingAttack = 1

    # Absinthe: generate and store randomized turn modifiers
    data.lEventRandomness[iLighthouseEarthQuake] = rand(40)
    data.lEventRandomness[iByzantiumVikingAttack] = rand(10)

    # Absinthe: rename cities on the 1200AD scenario - the WB file cannot handle special chars and long names properly
    #             some of the cities intentionally have different names though (compared to the CNM), for example some Kievan cities
    #             thus it's only set for Hungary for now, we can add more civs/cities later on if there are naming issues
    if get_scenario() == Scenario.i1200AD:
        for city in cities().owner(Civ.HUNGARY).entities():
            renameCities(city, Civ.HUNGARY)

    # Absinthe: refresh Dynamic Civ Names for all civs on the initial turn of the given scenario
    for iPlayer in civilizations().majors().ids():
        gc.getPlayer(iPlayer).processCivNames()
