from Consts import INDEPENDENT_CIVS
from PyUtils import any
import CoreFunctions as cf
import CoreTypes
from BaseStructures import BaseFactory, EnumDataMapper, Item, ItemCollection
from Errors import NotTypeExpectedError

try:
    from CvPythonExtensions import CyGlobalContext, CyPlayer, CyTeam, CyPlot, CyCity, CyUnit

    gc = CyGlobalContext()

except ImportError:
    gc = None

WORLD_WIDTH = 100
WORLD_HEIGHT = 73


class ScenarioDataMapper(EnumDataMapper):
    """Class to map data to Scenario enum."""

    BASE_CLASS = CoreTypes.Scenario


class ReligionDataMapper(EnumDataMapper):
    """Class to map Religion to Company enum."""

    BASE_CLASS = CoreTypes.Religion


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
        return player(self.key)

    @property
    def team(self):
        return team(self.key)

    @property
    def teamtype(self):
        return teamtype(self.key)

    @property
    def name(self):
        """Return the name of the civilization."""
        return name(self.key)

    @property
    def fullname(self):
        """Return the fullname of the civilization."""
        return fullname(self.key)

    @property
    def adjective(self):
        """Return the adjective of the civilization."""
        return adjective(self.key)

    def is_alive(self):
        """Return True if the civilization is alive."""
        return self.player.isAlive()

    def is_human(self):
        """Return True if the civilization is controlled by the player."""
        return self.player.isHuman()

    def is_existing(self):
        """Return True if the civilization is alive and have at least one city."""
        return self.player.isExisting()

    def is_main(self):
        """Return True if it's a main civilization, i.e. not minor and playable."""
        return is_main_civ(self)

    def is_major(self):
        """Return True if it's a major civilization, i.e. not minor ones (all playable and non-playable civs like The Pope)."""
        return is_major_civ(self)

    def is_minor(self):
        """Return True if it's a minor civilization, i.e. minor and not playable civs like independents and barbarian."""
        return is_minor_civ(self)

    def is_independent(self):
        """Return True if it's a non-playable independent civilization."""
        return is_independent_civ(self)

    def is_barbarian(self):
        """Return True if it's the barbarian."""
        return is_barbarian_civ(self)

    def state_religion(self):
        """Return state religion of the civilization."""
        return self.player.getStateReligion()

    def has_a_state_religion(self):
        """Return True if the civilization has a state religion."""
        return self.state_religion() != -1

    def has_state_religion(self, religion):
        """Return True if the civilization has the given religion as state religion."""
        return self.state_religion() == cf.religion(religion)

    def is_christian(self):
        """Return True if the civilization is christian."""
        return self.state_religion() in (
            CoreTypes.Religion.CATHOLICISM,
            CoreTypes.Religion.PROTESTANTISM,
            CoreTypes.Religion.ORTHODOXY,
        )

    def is_catholic(self):
        """Return True if the civilization is catholic."""
        return self.state_religion() == CoreTypes.Religion.CATHOLICISM

    def is_protestant(self):
        """Return True if the civilization is protestant."""
        return self.state_religion() == CoreTypes.Religion.PROTESTANTISM

    def is_orthodox(self):
        """Return True if the civilization is orthodox."""
        return self.state_religion() == CoreTypes.Religion.ORTHODOXY

    def is_muslim(self):
        """Return True if the civilization is muslim."""
        return self.state_religion() == CoreTypes.Religion.ISLAM

    def at_war(self, id):
        """Return True if the civilization is at war with `id`."""
        return self.team.isAtWar(teamtype(id))

    def declare_war(self, id):
        """Declare war with the civilization with `id`."""
        self.team.declareWar(teamtype(id), False, -1)

    def set_war(self, id):
        """Set war with the civilization with `id`.
        Instead of `declare_war`, `set_war` don't affect diplomatic relations."""
        self.team.setAtWar(teamtype(id), True)
        team(id).setAtWar(self.teamtype, True)

    def make_peace(self, id):
        """Make peace with the civilization with `id`."""
        self.team.makePeace(teamtype(id))

    def is_vassal(self, id):
        """Return True if the civilization is the vassal of `id`."""
        return self.team.isVassal(teamtype(id))

    def is_a_vassal(self):
        """Return True if the civilization is a vassal of another."""
        return self.team.isAVassal()

    def is_a_master(self):
        """Return True if the civilization is not a vassal."""
        return not self.is_a_vassal()

    def has_tech(self, id):
        """Return True if the civilization has the tech `id`."""
        return self.team.isHasTech(id)

    def add_tech(self, id, as_first=False, annoncing=False):
        """Add tech `id` to the civilization."""
        self.team.setHasTech(id.value, True, self.id, as_first, annoncing)

    def remove_tech(self, id):
        """Remove tech `id` to the civilization."""
        self.team.setHasTech(id.value, False, self.id, False, False)

    def has_open_borders(self, id):
        """Return True if the civilization has open borders with the civilization `id`."""
        return self.team.isOpenBorders(teamtype(id))

    def has_defensive_pact(self, id):
        """Return True if the civilization has defensive pact with the civilization `id`."""
        return self.team.isDefensivePact(teamtype(id))

    def has_meet(self, id):
        """Return True if the civilization has meet the civilization `id`."""
        return self.team.isHasMeet(teamtype(id))

    def send_gold(self, id, amount):
        """Send gold to the civilization `id`."""
        self.player.changeGold(-amount)
        player(id).changeGold(amount)


class Civilizations(ItemCollection):
    """A simple class to handle a set of civilizations."""

    BASE_CLASS = Civilization

    def alive(self):
        """Return alive civilizations."""
        return self.filter(lambda c: c.is_alive())

    def exists(self):
        """Return existing civilizations."""
        return self.filter(lambda c: c.is_existing())

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
        return self.filter(lambda c: c.is_main())

    def majors(self):
        """Return major civilizations, i.e. not minor ones (all playable and non-playable civs like The Pope)."""
        return self.filter(lambda c: c.is_major())

    def minors(self):
        """Return minor civilizations, i.e. minor and not playable civs like independents and barbarian."""
        return self.filter(lambda c: c.is_minor())

    def independents(self):
        """Return independents civilizations."""
        return self.filter(lambda c: c.is_independent())

    def barbarian(self):
        """Return the barbarian civilization."""
        return self.filter(lambda c: c.is_barbarian())

    def christian(self):
        """Retun all christian civilizations."""
        return self.filter(lambda c: c.is_christian())

    def catholic(self):
        """Retun all catholic civilizations."""
        return self.filter(lambda c: c.is_catholic())

    def protestant(self):
        """Retun all protestant civilizations."""
        return self.filter(lambda c: c.is_protestant())

    def orthodox(self):
        """Retun all orthodox civilizations."""
        return self.filter(lambda c: c.is_orthodox())

    def muslim(self):
        """Retun all islamic civilizations."""
        return self.filter(lambda c: c.is_muslim())

    def at_war(self, id):
        """Return all civilizations that are at war with `id`."""
        return self.filter(lambda c: c.at_war(id))

    def vassals(self):
        return self.filter(lambda c: any([c.is_vassal(other) for other in self]))

    def masters(self):
        return self.filter(lambda c: c not in self.vassals())

    def tech(self, id):
        """Return all civilization with the tech `id`."""
        return self.filter(lambda c: c.has_tech(id))

    def open_borders(self, id):
        """Return all civilization that have open borders with the civilization `id`."""
        return self.filter(lambda c: c.has_open_borders(id))

    def has_defensive_pact(self, id):
        """Return all civilization that have defensive pact with the civilization `id`."""
        return self.filter(lambda c: c.has_defensive_pact(id))

    def has_meet(self, id):
        """Return all civilization that have meet the civilization `id`."""
        return self.filter(lambda c: c.has_meet(id))


class CivilizationsFactory(BaseFactory):
    """A factory to generate `Civilizations`."""

    MEMBERS_CLASS = CoreTypes.Civ
    DATA_CLASS = CivDataMapper
    ITEM_CLASS = Civilization
    ITEM_COLLECTION_CLASS = Civilizations


def name(identifier):
    """Return the name of the civilization."""
    return player(identifier).getCivilizationShortDescription(0)


def fullname(identifier):
    """Return the fullname of the civilization."""
    return player(identifier).getCivilizationDescription(0)


def adjective(identifier):
    """Return the adjective of the civilization."""
    return player(identifier).getCivilizationAdjective(0)


def player(identifier=None):
    """Return CyPlayer object given an identifier."""
    if identifier is None:
        return gc.getActivePlayer()

    if isinstance(identifier, int):
        return gc.getPlayer(identifier)

    if isinstance(identifier, CoreTypes.Civ):
        return player(identifier.value)

    if isinstance(identifier, Civilization):
        return identifier.player

    if isinstance(identifier, CyPlayer):
        return identifier

    if isinstance(identifier, CyTeam):
        return gc.getPlayer(identifier.getLeaderID())

    if isinstance(identifier, (CyPlot, CyCity, CyUnit)):
        return gc.getPlayer(identifier.getOwner())

    raise NotTypeExpectedError(
        "CoreTypes.Civ, CyPlayer, CyTeam, CyPlot, CyCity, CyUnit, or int", type(identifier)
    )


def teamtype(identifier=None):
    """Return team ID given an identifier."""
    return player(identifier).getTeam()


def team(identifier=None):
    """Return CyTeam object given an identifier."""
    if identifier is None:
        return gc.getTeam(teamtype(identifier))

    if isinstance(identifier, int):
        return gc.getTeam(teamtype(identifier))

    if isinstance(identifier, CoreTypes.Civ):
        return team(identifier.value)

    if isinstance(identifier, Civilization):
        return identifier.team

    if isinstance(identifier, CyTeam):
        return identifier

    if isinstance(identifier, (CyPlayer, CyUnit, CyCity, CyPlot)):
        return gc.getTeam(identifier.getTeam())

    raise NotTypeExpectedError(
        "CoreTypes.Civ, CyPlayer, CyTeam, CyPlot, CyCity, CyUnit, or int", type(identifier)
    )


def human():
    """Return ID of the human player."""
    return gc.getGame().getActivePlayer()


def is_main_civ(identifier):
    """Return True if it's a main civilization, i.e. not minor and playable."""
    return player(identifier).isPlayable()


def is_major_civ(identifier):
    """Return True if it's a major civilization, i.e. not minor ones (all playable and non-playable civs like The Pope)."""
    return not is_minor_civ(identifier)


def is_minor_civ(identifier):
    """Return True if it's a minor civilization, i.e. minor and not playable civs like independents and barbarian."""
    return is_barbarian_civ(identifier) or is_independent_civ(identifier)


def is_independent_civ(identifier):
    """Return True if it's a non-playable independent civilization."""
    return cf.get_civ_by_id(player(identifier).getID()) in INDEPENDENT_CIVS


def is_barbarian_civ(identifier):
    """Return True if it's the barbarian."""
    return player(identifier).isBarbarian()


def period(identifier):
    """Return period given an identifier."""
    if identifier >= 0:
        return player(identifier).getPeriod()
    return None


class Tile(object):
    """class to handle a tile location."""

    def __init__(self, coordinates, **kwargs):
        if not isinstance(coordinates, tuple):
            raise NotTypeExpectedError(tuple, type(coordinates))
        self.coordinates = coordinates

        for name, value in kwargs.items():
            setattr(self, name, value)

    @property
    def x(self):
        return self.coordinates[0]

    @property
    def y(self):
        return self.coordinates[1]

    def to_tuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return self.__class__.__name__ + "(" + str(self.coordinates) + ")"

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, type(self)):
            return False
        return self.coordinates == other.coordinates

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


class Tiles(ItemCollection):
    """Class to handle a collection of tile."""

    BASE_CLASS = Tile


class TilesFactory:
    """A factory to generate `Tiles`."""

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
        if not isinstance(area, CoreTypes.AreaType):
            raise NotTypeExpectedError(CoreTypes.AreaType, type(area))
        for tile in self._results:
            tile.set_area(area)
        return self


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
        add_tiles = []

    if data.get(CoreTypes.Area.EXCEPTION_TILES) is not None:
        exception_tiles = [Tile(t) for t in data[CoreTypes.Area.EXCEPTION_TILES]]
    else:
        exception_tiles = []

    return {
        CoreTypes.Area.TILE_MIN: Tile(data[CoreTypes.Area.TILE_MIN]),
        CoreTypes.Area.TILE_MAX: Tile(data[CoreTypes.Area.TILE_MAX]),
        CoreTypes.Area.ADDITIONAL_TILES: add_tiles,
        CoreTypes.Area.EXCEPTION_TILES: exception_tiles,
    }
