from CvPythonExtensions import CyGlobalContext
from Consts import WORLD_HEIGHT, WORLD_WIDTH
from CoreFunctions import get_data_from_province_map, get_data_from_upside_down_map, location
from CoreFunctions import plot as _plot
from CoreFunctions import location as _location
from CoreData import civilizations
from CoreStructures import plots
from CoreTypes import Civ, PlagueType, ProvinceType, Religion, Technology
from LocationsData import LAKE_LOCATIONS
from CityMapData import CITIES_MAP
from ProvinceMapData import PROVINCES_MAP
from SettlerMapData import SETTLERS_MAP
from WarMapData import WARS_MAP

gc = CyGlobalContext()


def init():
    """Run in Handlers when the game starts."""
    init_player_variables()
    init_provinces()
    set_province_type_parameters()


def setup():
    init_player_maps()
    update_province_id()
    update_city_name()
    update_lake_id()
    update_core()
    set_vizualization_areas()


def init_player_variables():
    gc.setSizeNPlayers(
        WORLD_WIDTH,
        WORLD_HEIGHT,
        civilizations().majors().len(),
        civilizations().drop(Civ.BARBARIAN).len(),
        len(Technology),
        PlagueType.BUILDING_PLAGUE.value,
        len(Religion),
    )
    # set the Number of Provinces, call this before you set any AI or culture modifiers
    gc.setProvinceTypeNumber(len(ProvinceType))


def init_player_maps():
    for civ in civilizations().majors():
        for plot in plots().all().entities():
            x, y = location(plot)
            gc.setSettlersMap(civ.id, y, x, SETTLERS_MAP[civ.key][y][x])
            gc.setWarsMap(civ.id, y, x, WARS_MAP[civ.key][y][x])


def init_provinces():
    # for plot in plots().all().filter(lambda p: get_data_from_province_map(p) > -1).entities():
    for y in range(WORLD_HEIGHT):
        for x in range(WORLD_WIDTH):
            if PROVINCES_MAP[y][x] > -1:
                gc.setProvince(x, y, PROVINCES_MAP[y][x])
    gc.createProvinceCrossreferenceList()


def set_province_type_parameters():
    # How much culture should we get into a province of this type, ignore the war and settler values (0,0)
    gc.setProvinceTypeParams(ProvinceType.NONE.value, 0, 0, 1, 3)  # 1/3 culture
    gc.setProvinceTypeParams(ProvinceType.CONTESTED.value, 0, 0, 1, 1)  # no change to culture
    gc.setProvinceTypeParams(ProvinceType.POTENTIAL.value, 0, 0, 1, 1)  # same as outer culture
    gc.setProvinceTypeParams(ProvinceType.HISTORICAL.value, 0, 0, 2, 1)  # double-culture
    gc.setProvinceTypeParams(ProvinceType.CORE.value, 0, 0, 3, 1)  # triple-culture


def update_province_id():
    for plot in plots().all().entities():
        plot.setProvinceID(get_data_from_province_map(plot))


def update_city_name():
    for civ in civilizations().main():
        for plot in plots().all().entities():
            value = get_data_from_upside_down_map(CITIES_MAP, civ.id, plot)
            _plot(plot).setCityNameMap(civ.id, value)


def update_lake_id():
    for plot in plots().all().entities():
        for name, locations in LAKE_LOCATIONS.items():
            if _location(plot) in locations:
                value = name.value
            else:
                value = -1
            plot.setLakeNameID(value)


def update_core():
    for civ in civilizations().majors():
        core_tile_min = civ.location.area.core.tile_min
        core_tile_max = civ.location.area.core.tile_max
        core_additional_tiles = civ.location.area.core.additional_tiles
        normal_tile_min = civ.location.area.normal.tile_min
        normal_tile_max = civ.location.area.normal.tile_max
        normal_exception_tiles = civ.location.area.normal.exception_tiles
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
