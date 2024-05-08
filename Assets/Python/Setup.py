from CvPythonExtensions import CyGlobalContext
from CoreFunctions import get_data_from_province_map, get_data_from_upside_down_map
from CoreFunctions import plot as _plot
from CoreFunctions import location as _location
from CoreData import civilizations
from CoreStructures import year, plots
from LocationsData import LAKE_LOCATIONS
from CityMapData import CITIES_MAP
from TimelineData import TIMELINE_TECH_MODIFIER

gc = CyGlobalContext()


def setup():
    """Loads the data from RFCEMaps.py into appropriate objects within CvGameCoreDLL."""
    update_province_id()
    update_city_name()
    update_lake_id()
    update_core()
    set_vizualization_areas()
    set_tech_timeline_date()


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


def set_tech_timeline_date():
    for tech, turn in TIMELINE_TECH_MODIFIER:
        gc.setTimelineTechDateForTech(tech.value, year(turn))
