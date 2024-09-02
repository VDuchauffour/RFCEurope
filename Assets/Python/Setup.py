from CvPythonExtensions import CyGlobalContext
from CityNameManager import renameCities
from CoreTypes import Civ, Scenario, Area, AreaType
from PyUtils import rand
from StoredData import data
from Events import handler
from Consts import iLighthouseEarthQuake, iByzantiumVikingAttack
from Core import (
    civilizations,
    get_scenario,
    get_data_from_upside_down_map,
    get_data_from_province_map,
    location,
    log,
    plot as _plot,
    location as _location,
    plots,
    cities,
)
from LocationsData import LAKE_LOCATIONS
from CityMapData import CITIES_MAP
from SettlerMapData import SETTLERS_MAP
from WarMapData import WARS_MAP

gc = CyGlobalContext()


@handler("GameStart")
def setup_gamestart():
    setup()


@handler("OnLoad")
def setup_on_load():
    setup()


def setup():
    init_player_maps()
    update_core()
    set_vizualization_areas()
    update_province_id()
    update_city_name()
    update_lake_id()
    set_random_event()
    rename_cities_1200AD()
    refresh_dynamic_civ_name()
    log("RFCE: Setup.setup()")


def init_player_maps():
    for civ in civilizations().majors():
        for plot in plots.all().entities():
            x, y = location(plot)
            gc.setSettlersMap(civ.id, y, x, SETTLERS_MAP[civ.key][y][x])
            gc.setWarsMap(civ.id, y, x, WARS_MAP[civ.key][y][x])


def update_province_id():
    for plot in plots.all().entities():
        plot.setProvinceID(get_data_from_province_map(plot))


def update_city_name():
    for civ in civilizations().main():
        for plot in plots.all().entities():
            value = get_data_from_upside_down_map(CITIES_MAP, civ.id, plot)
            _plot(plot).setCityNameMap(civ.id, value)


def update_lake_id():
    for plot in plots.all().entities():
        for name, locations in LAKE_LOCATIONS.items():
            if _location(plot) in locations:
                value = name
            else:
                value = -1
            plot.setLakeNameID(value)


def update_core():
    for civ in civilizations().majors():
        core_tile_min = civ.location.area[AreaType.CORE][Area.TILE_MIN]
        core_tile_max = civ.location.area[AreaType.CORE][Area.TILE_MAX]
        core_additional_tiles = civ.location.area[AreaType.CORE][Area.ADDITIONAL_TILES]
        normal_tile_min = civ.location.area[AreaType.NORMAL][Area.TILE_MIN]
        normal_tile_max = civ.location.area[AreaType.NORMAL][Area.TILE_MAX]
        normal_exception_tiles = civ.location.area[AreaType.NORMAL][Area.EXCEPTION_TILES]
        gc.setCoreNormal(
            civ.id,
            core_tile_min[0],
            core_tile_min[1],
            core_tile_max[0],
            core_tile_max[1],
            normal_tile_min[0],
            normal_tile_min[1],
            normal_tile_max[0],
            normal_tile_max[1],
            len(core_additional_tiles),
            len(normal_exception_tiles),
        )
        for tile in core_additional_tiles:
            gc.addCoreException(civ.id, *tile)
        for tile in normal_exception_tiles:
            gc.addNormalException(civ.id, *tile)


def set_vizualization_areas():
    # Absinthe: separate visualization function for spawn and respawn areas
    # set it to 1 in the GlobalDefines_Alt.xml if you want to enable it
    # hold down the shift key, and hover over the map
    # hold down the alt key, and hover over the map
    gc.setCoreToPlot(gc.getDefineINT("ENABLE_SPAWN_AREA_DISPLAY"))
    gc.setNormalToPlot(gc.getDefineINT("ENABLE_RESPAWN_AREA_DISPLAY"))


def set_random_event():
    # Absinthe: generate and store randomized turn modifiers
    data.lEventRandomness[iLighthouseEarthQuake] = rand(40)
    data.lEventRandomness[iByzantiumVikingAttack] = rand(10)


def rename_cities_1200AD():
    # Absinthe: rename cities on the 1200AD scenario - the WB file cannot handle special chars and long names properly
    #             some of the cities intentionally have different names though (compared to the CNM), for example some Kievan cities
    #             thus it's only set for Hungary for now, we can add more civs/cities later on if there are naming issues
    if get_scenario() == Scenario.i1200AD:
        for city in cities.owner(Civ.HUNGARY).entities():
            renameCities(city, Civ.HUNGARY)


def refresh_dynamic_civ_name():
    # Absinthe: refresh Dynamic Civ Names for all civs on the initial turn of the given scenario
    for iPlayer in civilizations().majors().ids():
        gc.getPlayer(iPlayer).processCivNames()
