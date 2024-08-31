from CvPythonExtensions import CyGlobalContext
from Consts import WORLD_HEIGHT, WORLD_WIDTH
from Core import civilizations
from CoreTypes import Civ, PlagueType, ProvinceType, Religion, Technology
from ProvinceMapData import PROVINCES_MAP

gc = CyGlobalContext()


def init():
    init_player_variables()
    init_provinces()
    set_province_type_parameters()


def init_player_variables():
    gc.setSizeNPlayers(
        WORLD_WIDTH,
        WORLD_HEIGHT,
        civilizations().majors().len(),
        civilizations().drop(Civ.BARBARIAN).len(),
        len(Technology),
        PlagueType.BUILDING_PLAGUE,
        len(Religion),
    )
    # set the Number of Provinces, call this before you set any AI or culture modifiers
    gc.setProvinceTypeNumber(len(ProvinceType))


def init_provinces():
    # for plot in plots().all().filter(lambda p: get_data_from_province_map(p) > -1).entities():
    for y in range(WORLD_HEIGHT):
        for x in range(WORLD_WIDTH):
            if PROVINCES_MAP[y][x] > -1:
                gc.setProvince(x, y, PROVINCES_MAP[y][x])
    gc.createProvinceCrossreferenceList()


def set_province_type_parameters():
    # How much culture should we get into a province of this type, ignore the war and settler values (0,0)
    gc.setProvinceTypeParams(ProvinceType.NONE, 0, 0, 1, 3)  # 1/3 culture
    gc.setProvinceTypeParams(ProvinceType.CONTESTED, 0, 0, 1, 1)  # no change to culture
    gc.setProvinceTypeParams(ProvinceType.POTENTIAL, 0, 0, 1, 1)  # same as outer culture
    gc.setProvinceTypeParams(ProvinceType.HISTORICAL, 0, 0, 2, 1)  # double-culture
    gc.setProvinceTypeParams(ProvinceType.CORE, 0, 0, 3, 1)  # triple-culture
