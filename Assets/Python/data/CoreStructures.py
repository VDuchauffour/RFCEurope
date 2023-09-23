from CoreTypes import Civ, Scenario
from BaseStructures import EnumDataMapper
from Errors import NotTypeExpectedError

try:
    from CvPythonExtensions import CyGlobalContext

    gc = CyGlobalContext()

except ImportError:
    gc = None


class CivDataMapper(EnumDataMapper):
    """Class to map data to Civ enum."""

    BASE_CLASS = Civ


class ScenarioDataMapper(EnumDataMapper):
    """Class to map data to Scenario enum."""

    BASE_CLASS = Scenario


class Tile(tuple):
    """class to handle a tile location."""

    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]


class Tiles(list):
    """Class to handle a collection of tile."""

    def __init__(self, *tiles):
        for tile in tiles:
            if not isinstance(tile, Tile):
                raise ValueError("Must be a %s, received %s" % (Tile, type(tile)))
            self.append(tile)


def merge_tiles(*tiles_obj):
    """Merge multiple `Tiles` objects into a single one."""

    _tiles = Tiles()
    for obj in tiles_obj:
        if not isinstance(obj, Tiles):
            raise NotTypeExpectedError(Tiles, type(obj))
        for tile in obj:
            if not isinstance(tile, Tile):
                raise NotTypeExpectedError(Tile, type(tile))
            if tile not in _tiles:
                _tiles.append(tile)
    return _tiles


class TilesFactory:
    """A factory to generate `Tiles` from Area properties."""

    def __init__(self, x_max, y_max):
        self.data = Tiles()
        self.x_max = x_max
        self.y_max = y_max

    def rectangle(self, tile_min, tile_max):
        self.data += [
            Tile((x, y))
            for x in range(tile_min.x, tile_max.x + 1)
            for y in range(tile_min.y, tile_max.y + 1)
            if 0 <= x < self.x_max and 0 <= y < self.y_max
        ]
        return self

    def extend(self, additional_tiles):
        if additional_tiles is not None:
            self.data += additional_tiles
        return self

    def substract(self, exception_tiles):
        if exception_tiles is not None:
            self.data = list(filter(lambda t: t not in exception_tiles, self.data))
        return self

    def normalize(self):
        _data = Tiles()
        for data in self.data:
            if data not in _data:
                _data.append(data)
        self.data = _data
        return self


class Civilization(object):
    """A simple class to handle a civilization."""

    def __init__(self, id):
        if not isinstance(id, (int, Civ)):
            raise NotTypeExpectedError((int, Civ), type(id))
        self.id = int(id)

    def get_player(self):
        return gc.getPlayer(self.id)

    def get_team(self):
        return gc.getTeam(self.id)


# class Civilizations ???
