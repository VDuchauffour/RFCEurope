from CoreTypes import Area, AreaTypes, Civ, Scenario
from BaseStructures import EnumDataMapper
from Errors import NotACallableError, NotTypeExpectedError

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


class Tile(object):
    """class to handle a tile location."""

    def __init__(self, coordinates, areas=None):
        if areas is None:
            areas = []
        self._keys = {"coords": (coordinates[0], coordinates[1]), "areas": areas}

    @property
    def x(self):
        return self._keys["coords"][0]

    @property
    def y(self):
        return self._keys["coords"][1]

    @property
    def areas(self):
        return self._keys["areas"]

    def set_area(self, area):
        if not isinstance(area, AreaTypes):
            raise NotTypeExpectedError(AreaTypes, type(area))
        self._keys["areas"].append(area)

    def __str__(self):
        return str((self.x, self.y))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, type(self)):
            return False
        return self._keys == other._keys

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError("Cannot compare '%s' and '%s'" % (type(self), type(other)))
        if self.x > other.x or self.y > other.y:
            return True
        return False

    def __ge__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError("Cannot compare '%s' and '%s'" % (type(self), type(other)))
        if self.x >= other.x or self.y >= other.y:
            return True
        return False

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError("Cannot compare '%s' and '%s'" % (type(self), type(other)))
        if self.x < other.x or self.y < other.y:
            return True
        return False

    def __le__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError("Cannot compare '%s' and '%s'" % (type(self), type(other)))
        if self.x <= other.x or self.y <= other.y:
            return True
        return False


def parse_area_dict(data):
    """Parse a dict of area properties."""
    if data.get(Area.ADDITIONAL_TILES) is not None:
        add_tiles = [Tile(t) for t in data[Area.ADDITIONAL_TILES]]
    else:
        add_tiles = None

    if data.get(Area.EXCEPTION_TILES) is not None:
        exception_tiles = [Tile(t) for t in data[Area.EXCEPTION_TILES]]
    else:
        exception_tiles = None

    return {
        Area.TILE_MIN: Tile(data[Area.TILE_MIN]),
        Area.TILE_MAX: Tile(data[Area.TILE_MAX]),
        Area.ADDITIONAL_TILES: add_tiles,
        Area.EXCEPTION_TILES: exception_tiles,
    }


class Tiles(list):
    """Class to handle a collection of tile."""

    def __init__(self, *tiles):
        for tile in tiles:
            if not isinstance(tile, Tile):
                raise NotTypeExpectedError(Tile, type(tile))
            self.append(tile)

    def min(self):
        return min(self)

    def max(self):
        return max(self)


def normalize_tiles(tiles):
    """Merge multiple `Tiles` objects into a single one."""

    _tiles = Tiles()
    if not isinstance(tiles, Tiles):
        raise NotTypeExpectedError(Tiles, type(tiles))
    for tile in tiles:
        if not isinstance(tile, Tile):
            raise NotTypeExpectedError(Tile, type(tile))
        if tile not in _tiles:
            _tiles.append(tile)
    return _tiles


def concat_tiles(*tiles_obj):
    """Concat multiple `Tiles` objects into a single one."""

    _tiles = Tiles()
    for obj in tiles_obj:
        if not isinstance(obj, Tiles):
            raise NotTypeExpectedError(Tiles, type(obj))
        _tiles += obj
    return _tiles


class TilesFactory:
    """A factory to generate `Tiles` from Area properties."""

    def __init__(self, x_max, y_max):
        self._results = Tiles()
        self.x_max = x_max
        self.y_max = y_max

    def import_tiles(self, tiles):
        if not isinstance(tiles, Tiles):
            raise NotTypeExpectedError(Tiles, type(tiles))
        self._results = tiles
        return self

    def get_results(self):
        return self._results

    def rectangle(self, tile_min, tile_max):
        self._results += [
            Tile((x, y))
            for x in range(tile_min.x, tile_max.x + 1)
            for y in range(tile_min.y, tile_max.y + 1)
            if 0 <= x < self.x_max and 0 <= y < self.y_max
        ]
        return self

    def extend(self, additional_tiles):
        if additional_tiles is not None:
            self._results += additional_tiles
        return self

    def substract(self, exception_tiles):
        if exception_tiles is not None:
            self._results = list(filter(lambda t: t not in exception_tiles, self._results))
        return self

    def normalize(self):
        _data = Tiles()
        for data in self._results:
            if data not in _data:
                _data.append(data)
        self._results = _data
        return self

    def attach_area(self, area):
        if not isinstance(area, AreaTypes):
            raise NotTypeExpectedError(AreaTypes, type(area))
        for tile in self._results:
            tile.set_area(area)
        return self


class CivilizationProperties(object):
    def __init__(self, **properties):
        for property in properties.items():
            name, value = property
            setattr(self, name, value)

    def __repr__(self):
        return self.__class__.__name__ + "(" + str(self.__dict__) + ")"


class Civilization(object):
    """A simple class to handle a civilization."""

    def __init__(self, id, properties):
        if not isinstance(id, Civ):
            raise NotTypeExpectedError(Civ, type(id))
        self._id = id
        self.properties = properties

    @property
    def id(self):
        return self._id.value  # type: ignore

    @property
    def key(self):
        return self._id

    @property
    def name(self):
        return self._id.name  # type: ignore

    def __repr__(self):
        return self.__class__.__name__ + "(" + str(Civ[self.name]) + ")"

    def get_player(self):
        return gc.getPlayer(self.id)

    def get_team(self):
        return gc.getTeam(self.id)


class Civilizations(list):
    """A simple class to handle a set of civilizations."""

    def __init__(self, *civs):
        for civ in civs:
            if not isinstance(civ, Civilization):
                raise NotTypeExpectedError(Civilization, type(civ))
            self.append(civ)

    def filter(self, func):
        """Filter civilization when function returns `True`."""
        if not callable(func):
            raise NotACallableError(func)
        return [civ for civ in self if func(civ)]

    def get_main(self):
        """Return main civilizations, i.e. not minor and playable."""
        return self.filter(lambda c: c.properties.is_playable and not c.properties.is_minor)

    def get_majors(self):
        """Return major civilizations, i.e. not minor ones (all playable and non-playable civs like The Pope)."""
        return self.filter(lambda c: not c.properties.is_minor)

    def get_minors(self):
        """Return minor civilizations, i.e. minor and not playable."""
        return self.filter(lambda c: c.properties.is_minor and not c.properties.is_playable)
