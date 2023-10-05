from CoreTypes import Area, AreaTypes, Civ, Religion, Scenario
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

    def to_tuple(self):
        return (self.x, self.y)

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


class CivilizationAttributes(object):
    """A class to handle civilization attibutes from CivDataMapper."""

    def __init__(self, **properties):
        for name, value in properties.items():
            setattr(self, name, value)

    def __repr__(self):
        return self.__class__.__name__ + "(" + str(self.__dict__) + ")"


class Civilization(object):
    """A simple class to handle a civilization."""

    def __init__(self, id, **kwargs):
        if not isinstance(id, Civ):
            raise NotTypeExpectedError(Civ, type(id))
        self._id = id
        for name, value in kwargs.items():
            setattr(self, name, value)

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

    @property
    def player(self):
        return gc.getPlayer(self.id)

    @property
    def team(self):
        return gc.getTeam(self.id)


def get_enum_by_id(enum, id):
    """Return a enum member by its index."""
    return enum[enum._member_names_[id]]


def get_civ_by_id(id):
    """Return a Civ member by its index."""
    return get_enum_by_id(Civ, id)


def get_religion_by_id(id):
    """Return a Religion member by its index."""
    return get_enum_by_id(Religion, id)


class Civilizations(list):
    """A simple class to handle a set of civilizations."""

    def __init__(self, *civs):
        for civ in civs:
            if not isinstance(civ, Civilization):
                raise NotTypeExpectedError(Civilization, type(civ))
            self.append(civ)

    def len(self):
        return self.__len__()

    def ids(self):
        """Return a list of identifiers."""
        return [civ.id for civ in self]

    def filter(self, func):
        """Filter civilization when function returns `True`."""
        if not callable(func):
            raise NotACallableError(func)
        civs = [civ for civ in self if func(civ)]
        return self.__class__(*civs)

    def drop(self, *civs):
        """Return the object without `civs` given its keys, i.e. the relevant `Civ` member."""
        return self.filter(lambda c: c.key not in civs)

    def get(self, *civs):
        """Return the object with only `civs` given its keys, i.e. the relevant `Civ` member."""
        return self.filter(lambda c: c.key in civs)

    def main(self):
        """Return main civilizations, i.e. not minor and playable."""
        return self.filter(lambda c: c.properties.is_playable and not c.properties.is_minor)

    def majors(self):
        """Return major civilizations, i.e. not minor ones (all playable and non-playable civs like The Pope)."""
        return self.filter(lambda c: not c.properties.is_minor)

    def minors(self):
        """Return minor civilizations, i.e. minor and not playable civs like independents and barbarian."""
        return self.filter(lambda c: c.properties.is_minor and not c.properties.is_playable)

    def independents(self):
        """Return independents civilizations."""
        return self.filter(lambda c: "INDEPENDENT" in c.name)

    def barbarian(self):
        """Return the barbarian civilization."""
        return self.get(Civ.BARBARIAN)[0]

    # TODO add func for any, all, where cf https://github.com/dguenms/Dawn-of-Civilization/blob/a305e7846d085d6edf1e9c472e8dfceee1c07dd4/Assets/Python/Core.py#L1683


class CivilizationsFactory(object):
    """A factory to generate `Civilizations` from CivDataMapper."""

    def __init__(self):
        self._attachments = {}

    def attach(self, name, data):
        if isinstance(name, str) and isinstance(data, CivDataMapper):
            self._attachments[name] = data
        return self

    def collect(self):
        civs = []
        for civ in Civ:
            attachments = dict((k, v[civ]) for k, v in self._attachments.items())
            civs.append(Civilization(civ, **attachments))
        return Civilizations(*civs)
