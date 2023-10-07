import random
import CoreTypes
from PyUtils import all, any
from BaseStructures import EnumDataMapper
from Enum import Enum
from Errors import NotACallableError, NotTypeExpectedError

try:
    from CvPythonExtensions import CyGlobalContext

    gc = CyGlobalContext()

except ImportError:
    gc = None


class CivDataMapper(EnumDataMapper):
    """Class to map data to Civ enum."""

    BASE_CLASS = CoreTypes.Civ


class CompanyDataMapper(EnumDataMapper):
    """Class to map data to Company enum."""

    BASE_CLASS = CoreTypes.Company


class ScenarioDataMapper(EnumDataMapper):
    """Class to map data to Scenario enum."""

    BASE_CLASS = CoreTypes.Scenario


class Attributes(dict):
    """A class to handle attibutes from a DataMapper."""

    def __init__(self, **properties):
        for name, value in properties.items():
            setattr(self, name, value)

    def __repr__(self):
        return self.__class__.__name__ + "(" + str(self.__dict__) + ")"


class Item(object):
    """A base class to handle a game item."""

    BASE_CLASS = None

    def __init__(self, id, **kwargs):
        if not issubclass(self.BASE_CLASS, Enum):
            raise NotTypeExpectedError(Enum, self.BASE_CLASS)

        if not isinstance(id, self.BASE_CLASS):
            raise NotTypeExpectedError(self.BASE_CLASS, type(id))

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
        return self.__class__.__name__ + "(" + str(self.BASE_CLASS[self.name]) + ")"


class ItemCollection(list):
    """A base class to handle a set of a specific type of `Item`."""

    BASE_CLASS = None

    def __init__(self, *items):
        for item in items:
            if not isinstance(item, self.BASE_CLASS):
                raise NotTypeExpectedError(self.BASE_CLASS, type(item))
            self.append(item)

    def len(self):
        return self.__len__()

    def copy(self, *items):
        return self.__class__(*items)

    def _apply(self, condition):
        if not callable(condition):
            raise NotACallableError(condition)
        return [condition(item) for item in self]

    def _compress(self, selectors, negate=False):
        if negate:
            return (item for item, s in zip(self, selectors) if not s)
        return (item for item, s in zip(self, selectors) if s)

    def _filter(self, condition):
        return self._compress(self._apply(condition))

    def filter(self, condition):
        """Filter item when `condition` is True."""
        return self.copy(*self._filter(condition))

    def attributes(self, attribute):
        """Return a list of item attribute."""
        return self._apply(attribute)

    def ids(self):
        """Return a list of identifiers."""
        return self.attributes(lambda c: c.id)

    def split(self, condition):
        """Return a tuple of 2 elements, the first corresponds to items where `condition` is True, the second not."""
        status = self._apply(condition)
        valid_items = self._compress(status)
        rest_items = self._compress(status, negate=True)
        return (self.copy(*valid_items), self.copy(*rest_items))

    def all(self, condition):
        """Return True if `condition` is True for all items."""
        return all(self._apply(condition))

    def any(self, condition):
        """Return True if `condition` is True for at least one items."""
        return any(self._apply(condition))

    def none(self, condition):
        """Return True if `condition` is False for all items."""
        return not self.any(condition)

    def drop(self, *items):
        """Return the object without `items` given its keys, i.e. the relevant enum member."""
        return self.filter(lambda x: x.key not in items)

    def take(self, *items):
        """Return the object with only `items` given its keys, i.e. the relevant enum member."""
        return self.filter(lambda x: x.key in items)

    def limit(self, n):
        """Return the first `n` items of the object."""
        return self[:n]

    def sort(self, metric, reverse=False):
        """Return the object sorted given a `metric` function."""
        return self.copy(*sorted(self, key=metric, reverse=reverse))

    def nlargest(self, n, metric):
        """Return the first `n` largest item of the object given a `metric` function."""
        return self.sort(metric, reverse=True).limit(n)

    def nsmallest(self, n, metric):
        """Return the first `n` smallest item of the object given a `metric` function."""
        return self.sort(metric).limit(n)

    def maximum(self, metric):
        """Return the largest item of the object given a `metric` function."""
        return self.nlargest(1, metric)

    def minimum(self, metric):
        """Return the smallest item of the object given a `metric` function."""
        return self.nsmallest(1, metric)

    def random(self):
        """Return a single entry of the object."""
        return self.copy(random.choice(self))

    def sample(self, k):
        """Return a sample of the object."""
        return self.copy(*random.sample(self, k))


class Company(Item):
    """A simple class to handle a company."""

    BASE_CLASS = CoreTypes.Company


class Companies(ItemCollection):
    """A simple class to handle a set of companies."""

    BASE_CLASS = Company


class Civilization(Item):
    """A simple class to handle a civilization."""

    BASE_CLASS = CoreTypes.Civ

    @property
    def player(self):
        return gc.getPlayer(self.id)

    @property
    def team(self):
        return gc.getTeam(self.id)

    @property
    def description(self):
        return self.player.getCivilizationShortDescription(0)

    @property
    def long_description(self):
        return self.player.getCivilizationDescription(0)

    @property
    def adjective(self):
        return self.player.getCivilizationAdjective(0)


class Civilizations(ItemCollection):
    """A simple class to handle a set of civilizations."""

    BASE_CLASS = Civilization

    def alive(self):
        """Return alive civilizations."""
        return self.filter(lambda c: c.player.isAlive())

    def dead(self):
        """Return dead civilizations."""
        return self.filter(lambda c: not c.player.isAlive())

    def existing(self):
        """Return existing civilizations."""
        return self.filter(lambda c: c.player.isExisting())

    def inexisting(self):
        """Return inexisting civilizations."""
        return self.filter(lambda c: not c.player.isExisting())

    def ai(self):
        """Return civilizations played by AI."""
        return self.filter(lambda c: not c.player.isHuman())

    def human(self):
        """Return civilization of the player."""
        return self.filter(lambda c: c.player.isHuman())

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
        return self.take(CoreTypes.Civ.BARBARIAN)[0]


class BaseFactory(object):
    """A base for factories."""

    MEMBERS_CLASS = None
    DATA_CLASS = None
    ITEM_CLASS = None
    ITEM_COLLECTION_CLASS = None

    def __init__(self):
        self._attachments = {}

    def attach(self, name, data):
        if isinstance(name, str) and isinstance(data, self.DATA_CLASS):
            self._attachments[name] = data
        return self

    def collect(self):
        items = []
        for member in self.MEMBERS_CLASS:
            attachments = dict((k, v[member]) for k, v in self._attachments.items())
            items.append(self.ITEM_CLASS(member, **attachments))
        return self.ITEM_COLLECTION_CLASS(*items)


class CompaniesFactory(BaseFactory):
    """A factory to generate `Companies`."""

    MEMBERS_CLASS = CoreTypes.Company
    DATA_CLASS = CompanyDataMapper
    ITEM_CLASS = Company
    ITEM_COLLECTION_CLASS = Companies


class CivilizationsFactory(BaseFactory):
    """A factory to generate `Civilizations`."""

    MEMBERS_CLASS = CoreTypes.Civ
    DATA_CLASS = CivDataMapper
    ITEM_CLASS = Civilization
    ITEM_COLLECTION_CLASS = Civilizations


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
        if not isinstance(area, CoreTypes.AreaTypes):
            raise NotTypeExpectedError(CoreTypes.AreaTypes, type(area))
        self._keys["areas"].append(area)

    def __str__(self):
        return str(self.to_tuple())

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
        if not isinstance(area, CoreTypes.AreaTypes):
            raise NotTypeExpectedError(CoreTypes.AreaTypes, type(area))
        for tile in self._results:
            tile.set_area(area)
        return self


def get_enum_by_id(enum, id):
    """Return a enum member by its index."""
    return enum[enum._member_names_[id]]


def get_civ_by_id(id):
    """Return a Civ member by its index."""
    return get_enum_by_id(CoreTypes.Civ, id)


def get_religion_by_id(id):
    """Return a Religion member by its index."""
    return get_enum_by_id(CoreTypes.Religion, id)


def attribute_factory(data):
    """Return a `Attributes` object given Mapping with enum member as keys."""
    return Attributes(**dict((k.name.lower(), v) for k, v in data.items()))


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


def concat_tiles(*tiles):
    """Concat multiple `Tiles` objects into a single one."""

    _tiles = Tiles()
    for obj in tiles:
        if not isinstance(obj, Tiles):
            raise NotTypeExpectedError(Tiles, type(obj))
        _tiles += obj
    return _tiles


def parse_area_dict(data):
    """Parse a dict of area properties."""
    if data.get(CoreTypes.Area.ADDITIONAL_TILES) is not None:
        add_tiles = [Tile(t) for t in data[CoreTypes.Area.ADDITIONAL_TILES]]
    else:
        add_tiles = None

    if data.get(CoreTypes.Area.EXCEPTION_TILES) is not None:
        exception_tiles = [Tile(t) for t in data[CoreTypes.Area.EXCEPTION_TILES]]
    else:
        exception_tiles = None

    return {
        CoreTypes.Area.TILE_MIN: Tile(data[CoreTypes.Area.TILE_MIN]),
        CoreTypes.Area.TILE_MAX: Tile(data[CoreTypes.Area.TILE_MAX]),
        CoreTypes.Area.ADDITIONAL_TILES: add_tiles,
        CoreTypes.Area.EXCEPTION_TILES: exception_tiles,
    }
