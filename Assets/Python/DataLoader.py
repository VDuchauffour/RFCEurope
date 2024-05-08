from CoreFunctions import get_data_from_province_map, get_data_from_upside_down_map
from CoreFunctions import plot as _plot
from CoreFunctions import location as _location
from CoreData import civilizations
from CoreStructures import plots
from LocationsData import LAKE_LOCATIONS
from CityMapData import CITIES_MAP


def setup():
    """Loads the data from RFCEMaps.py into appropriate objects within CvGameCoreDLL."""
    update_province_id()
    update_city_name()
    update_lake_id()


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
