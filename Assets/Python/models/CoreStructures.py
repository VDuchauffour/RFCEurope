import CoreTypes
from BaseStructures import Attributes, BaseFactory, EnumDataMapper, Item, ItemCollection
from Errors import NotTypeExpectedError

try:
    from CvPythonExtensions import CyGlobalContext

    gc = CyGlobalContext()

except ImportError:
    gc = None


class ScenarioDataMapper(EnumDataMapper):
    """Class to map data to Scenario enum."""

    BASE_CLASS = CoreTypes.Scenario


class CompanyDataMapper(EnumDataMapper):
    """Class to map data to Company enum."""

    BASE_CLASS = CoreTypes.Company


class Company(Item):
    """A simple class to handle a company."""

    BASE_CLASS = CoreTypes.Company


class Companies(ItemCollection):
    """A simple class to handle a set of companies."""

    BASE_CLASS = Company


class CompaniesFactory(BaseFactory):
    """A factory to generate `Companies`."""

    MEMBERS_CLASS = CoreTypes.Company
    DATA_CLASS = CompanyDataMapper
    ITEM_CLASS = Company
    ITEM_COLLECTION_CLASS = Companies


class CivDataMapper(EnumDataMapper):
    """Class to map data to Civ enum."""

    BASE_CLASS = CoreTypes.Civ


class Civilization(Item):
    """A simple class to handle a civilization."""

    BASE_CLASS = CoreTypes.Civ

    @property
    def player(self):
        return gc.getPlayer(self.id)

    @property
    def team(self):
        return gc.getTeam(self.player.getTeam())

    @property
    def player_id(self):
        return self.player.getID()

    @property
    def team_id(self):
        return self.team.getID()

    @property
    def description(self):
        return self.player.getCivilizationShortDescription(0)

    @property
    def long_description(self):
        return self.player.getCivilizationDescription(0)

    @property
    def adjective(self):
        return self.player.getCivilizationAdjective(0)

    def is_alive(self):
        """Return True if the civilization is alive."""
        return self.player.isAlive()

    def is_human(self):
        """Return True if the civilization is controlled by the player."""
        return self.player.isHuman()

    def state_religion(self):
        """Return state religion of the civilization."""
        return self.player.getStateReligion()

    def has_state_religion(self):
        """Return True if the civilization has no state religion."""
        return self.state_religion() == -1

    def is_christian(self):
        """Return True if the civilization is christian."""
        return self.state_religion() in (
            CoreTypes.Religion.CATHOLICISM,
            CoreTypes.Religion.PROTESTANTISM,
            CoreTypes.Religion.ORTHODOXY,
        )

    def is_muslim(self):
        """Return True if the civilization is muslim."""
        return self.state_religion() == CoreTypes.Religion.ISLAM

    def at_war(self, id):
        """Return True if the civilization is at war with `id`."""
        if isinstance(id, CoreTypes.Civ):
            id = self.__class__(id)
        return self.team.isAtWar(id.team_id)


class Civilizations(ItemCollection):
    """A simple class to handle a set of civilizations."""

    BASE_CLASS = Civilization

    def alive(self):
        """Return alive civilizations."""
        return self.filter(lambda c: c.is_alive())

    def dead(self):
        """Return dead civilizations."""
        return self.filter(lambda c: not c.is_alive())

    def ai(self):
        """Return civilizations played by AI."""
        return self.filter(lambda c: not c.is_human())

    def human(self):
        """Return civilization of the player."""
        return self.filter(lambda c: c.is_human())

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

    def christian(self):
        """Retun all christian civilizations."""
        return self.filter(lambda c: c.is_christian())

    def muslim(self):
        """Retun all islamic civilizations."""
        return self.filter(lambda c: c.is_muslim())

    def at_war(self, id):
        """Return all civilizations that are at war with `id`."""
        return self.filter(lambda c: c.team.isAtWar(self[id].team))


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
