# from BugEventManager import g_eventManager as events

from CivilizationsData import (
    CIV_ADDITIONAL_UNITS,
    CIV_AI_MODIFIERS,
    CIV_AI_REFORMATION_THRESHOLD,
    CIV_AI_STOP_BIRTH_THRESHOLD,
    CIV_HIRE_MERCENARY_THRESHOLD,
    CIV_HUMAN_MODIFIERS,
    CIV_INITIAL_BUILDINGS,
    CIV_INITIAL_CONTACTS,
    CIV_INITIAL_TECH,
    CIV_INITIAL_UNITS,
    CIV_INITIAL_WARS,
    CIV_INITIAL_WORKERS,
    CIV_LEADERS,
    CIV_RELIGION_SPREADING_THRESHOLD,
    CIV_RELIGIOUS_TOLERANCE,
    CIV_RESPAWNING_THRESHOLD,
    CIV_SCENARIO_CONDITION,
    CIV_STABILITY_AI_BONUS,
)
from Consts import INDEPENDENT_CIVS, WORLD_HEIGHT, WORLD_WIDTH, MessageData
from CoreTypes import Civ, Scenario
from LocationsData import (
    CIV_AREAS,
    CIV_CAPITAL_LOCATIONS,
    CIV_EVENT_DRIVE_PROVINCES,
    CIV_HOME_LOCATIONS,
    CIV_NEIGHBOURS,
    CIV_NEW_CAPITAL_LOCATIONS,
    CIV_PROVINCES,
    CIV_REFORMATION_NEIGHBOURS,
    CIV_VISIBLE_AREA,
    COMPANY_REGION,
)
from MiscData import COMPANY_LIMIT
from ProvinceMapData import PROVINCES_MAP
from PyUtils import (
    all,
    any,
    none,
    rand,
    attrgetter,
    choices,
    combinations,
    permutations,
    product,
    random_entry,
)
from itertools import groupby
import random
from copy import deepcopy
import CoreTypes
from DataStructures import (
    CivDataMapper,
    CompanyDataMapper,
    Attributes,
    sort,
)
from Errors import NotTypeExpectedError, NotACallableError
from Enum import Enum
from TimelineData import (
    CIV_BIRTHDATE,
    CIV_COLLAPSE_DATE,
    CIV_RESPAWNING_DATE,
    COMPANY_BIRTHDATE,
    COMPANY_DEATHDATE,
)

try:
    from CvPythonExtensions import (
        CyGlobalContext,
        CyTranslator,
        CyInterface,
        CyPlayer,
        CyTeam,
        CyPlot,
        CyCity,
        CyUnit,
        CyGame,
        CvBonusInfo,
        CvBuildInfo,
        CvBuildingInfo,
        CvBuildingClassInfo,
        CvCivilizationInfo,
        CvCommerceInfo,
        CvCorporationInfo,
        CvCultureLevelInfo,
        CvEraInfo,
        CvFeatureInfo,
        CvGameSpeedInfo,
        CvHandicapInfo,
        CvImprovementInfo,
        CvLeaderHeadInfo,
        CvPromotionInfo,
        CvProjectInfo,
        CvReligionInfo,
        CvRouteInfo,
        CvSpecialistInfo,
        CvTechInfo,
        CvTerrainInfo,
        CvUnitInfo,
        UnitCombatTypes,
        getTurnForYear,
        AttitudeTypes,
        CommerceTypes,
        ColorTypes,
        DomainTypes,
        UnitAITypes,
        DirectionTypes,
        EventContextTypes,
        PlayerTypes,
        TeamTypes,
        plotDistance,
        stepDistance,
    )
    import Popup

    gc = CyGlobalContext()
    game = gc.getGame()
    translator = CyTranslator()
    interface = CyInterface()

except ImportError:
    gc = None
    game = None
    translator = None
    interface = None


class Item(object):
    """A base class to handle a game item backed with enum."""

    BASE_CLASS = None

    def __init__(self, id, **kwargs):
        if not issubclass(self.BASE_CLASS, Enum):  # type: ignore
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
    def id_name(self):
        return self._id.name  # type: ignore

    def __repr__(self):
        return self.__class__.__name__ + "(" + str(self.BASE_CLASS[self.id_name]) + ")"

    def copy(self, **kwargs):
        return self.__class__(self.key, **kwargs)


class Collection(list):
    """A base class to handle a set of game item."""

    def __init__(self, *items):
        for item in items:
            self.append(item)

    def len(self):
        return self.__len__()

    def copy(self, *items):
        return self.__class__(*items)

    def empty(self):
        return self.copy(*[])

    def first(self):
        """Return the first item of the collection."""
        return self[0]

    def last(self):
        """Return the last item of the collection."""
        return self[-1]

    def unwrap(self):
        """Unwrap items of the collection."""
        if len(self) == 1:
            return self.first()
        return self

    def apply(self, condition):
        if not callable(condition):
            raise NotACallableError(condition)
        return [condition(item) for item in self]

    def _compress(self, selectors, negate=False):
        if negate:
            return (item for item, s in zip(self, selectors) if not s)
        return (item for item, s in zip(self, selectors) if s)

    def _filter(self, condition):
        return self._compress(self.apply(condition))

    def filter(self, condition):
        """Filter item when `condition` is True."""
        return self.copy(*self._filter(condition))

    def transform(self, cls, map=lambda x: x, condition=lambda x: True):
        """Return new class given a map function and a condition function."""
        return cls([map(k) for k in self if condition(k)])

    @staticmethod
    def __handle_string_args(strings):
        if isinstance(strings, str):
            strings = [strings]
        if not isinstance(strings, (tuple, list)):
            raise ValueError("`attributes` must be a list or a tuple, received %s" % type(strings))
        return strings

    def _select(self, attributes):
        items = []
        obj = deepcopy(self)
        for item in obj:
            for attr in item.__dict__.keys():
                if not attr.startswith("_") and attr not in attributes:
                    item.__dict__.pop(attr, None)
            items.append(item)
        return self.copy(*items)

    def select(self, attributes):
        """Return the object with selected attributes of items. `attributes` can be a single attribute or a sequence of attributes.
        Only works with a primary key, using nested keys do not work."""
        attributes = self.__handle_string_args(attributes)
        return self._select(attributes)

    @staticmethod
    def _dropna(data, attribute):
        """Return True if any subkey of data is not None or the value is not None."""
        f = attrgetter(attribute)
        attr = f(data)
        if issubclass(attr.__class__, dict):
            return any([v is not None for v in attr.values()])
        else:
            return attr is not None

    def dropna(self, attributes):  # TODO to move to enum collection ?
        """Return the object without those that have None as the value for the `attribute`.
        Only works with a primary key, using nested keys do not work."""
        attributes = self.__handle_string_args(attributes)
        obj = deepcopy(self)
        for attribute in attributes:
            obj = obj.filter(lambda c: self._dropna(c, attribute))
        return obj

    def split(self, condition):
        """Return a tuple of 2 elements, the first corresponds to items where `condition` is True, the second not."""
        status = self.apply(condition)
        valid_items = self._compress(status)
        rest_items = self._compress(status, negate=True)
        return (self.copy(*valid_items), self.copy(*rest_items))

    def all(self, condition):
        """Return True if `condition` is True for all items."""
        return all(self.apply(condition))

    def any(self, condition):
        """Return True if `condition` is True for at least one items."""
        return any(self.apply(condition))

    def none(self, condition):
        """Return True if `condition` is False for all items."""
        return not self.any(condition)

    def drop(self, *items):  # TODO this should be renamed to without
        """Return the object without `items` given its item."""
        return self.filter(lambda x: x not in items)

    def take(self, *items):
        """Return the object with only `items` given its item."""
        return self.filter(lambda x: x in items)

    def unique(self):
        """Return only unique items."""
        return self.copy(*[k for k in set(self)])

    def enrich(self, func):
        """Return an enriched version of the object given a function."""
        enrich = self.copy(*[])
        for key in self:
            enrich += func(key)
        enriched = self + enrich
        return enriched.unique()

    def limit(self, n):
        """Return the first `n` items of the object."""
        return self[:n]

    def groupby(self, func):
        """Return the grouped collection given a function."""
        return [
            (key, self.copy(*group))
            for key, group in groupby(self.sort(func), lambda key: func(key))
        ]

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

    def rank(self, key, metric):
        """Return the ranked collection given a `metric` function."""
        sorted_keys = sort(self, lambda k: metric(k), True)
        return sorted_keys.index(key)

    def random(self, weights=None, k=1):
        """Return a k sized list of items."""
        return self.copy(*choices(self, weights, k=k))

    def random_entry(self):
        """Return a single random item. Return None if no entries available."""
        return random_entry(self)

    def shuffle(self):
        """Return the object with the shuffled items."""
        return self.copy(*random.shuffle(self))

    def sample(self, k):
        """Return a sample of the object."""
        return self.copy(*random.sample(self, k))

    def product(self, other=None, repeat=1):
        """Return catersian product of the object."""
        if other is None:
            other = self
            print(type(other), other)
        return product(repeat, self, other)

    def permutations(self, repeat=2):
        """Return successive `repeat` length permutations of the object."""
        return permutations(self, repeat)

    def combinations(self, repeat=2):
        """Return `repeat` length subsequences of the object."""
        return combinations(self, repeat)


class EntitiesCollection(Collection):
    """A base class to handle a set of game item taken from RFC DoC."""

    def _keyify(self, item):
        """Inner function for retrieving the in-game items of the entity."""
        return item

    def _factory(self, key):
        """Inner function for producing the in-game class of the entity."""
        return key

    def entities(self):
        """Retrieve in-game item of the collection."""
        return [self._factory(x) for x in self]

    def __getitem__(self, index):
        return self.entities()[index]

    # def __iter__(self):  # TODO currently recursive loop, we should using the _keys attribute paradigm
    #     return iter(self.entities())

    def __add__(self, other):
        if other is None:
            return self
        if not isinstance(other, type(self)):
            raise TypeError("Cannot combine left '%s' with right '%s'" % (type(self), type(other)))
        items = [s for s in self] + [o for o in other]
        return self.copy(*items)

    def add(self, other):
        return self.__add__(other)

    def apply(self, condition):
        if not callable(condition):
            raise NotACallableError(condition)
        return [condition(self._factory(item)) for item in self]

    def sort(self, metric, reverse=False):
        """Return the object sorted given a `metric` function."""
        return self.copy(*sorted(self, key=lambda x: metric(self._factory(x)), reverse=reverse))

    def transform(self, cls, map=lambda x: x, condition=lambda x: True):
        """Return new class given a map function and a condition function."""
        return cls(*[map(k) for k in self if condition(self._factory(k))])

    def groupby(self, func):
        """Return the grouped collection given a function."""
        return [
            (key, self.copy(*group))
            for key, group in groupby(self.sort(func), lambda key: func(self._factory(key)))
        ]

    def rank(self, key, metric):
        """Return the ranked collection given a `metric` function."""
        sorted_keys = sort(self._keys, lambda k: metric(self._factory(k)), True)
        return sorted_keys.index(key)


class EnumCollection(Collection):
    """A base class to handle a set of a specific type of `Item`."""

    BASE_CLASS = None

    def __init__(self, *items):
        for item in items:
            if not isinstance(item, self.BASE_CLASS):  # type: ignore
                raise NotTypeExpectedError(self.BASE_CLASS, type(item))
            self.append(item)

    def drop(self, *items):  # TODO this should be renamed to without
        """Return the object without `items` given its keys, i.e. the relevant enum member."""
        return self.filter(lambda x: x.key not in items)

    def take(self, *items):
        """Return the object with only `items` given its keys, i.e. the relevant enum member."""
        return self.filter(lambda x: x.key in items)

    def ids(self):
        """Return a list of identifiers."""
        return self.apply(lambda c: c.id)


class EnumCollectionFactory(object):
    """A base for factories."""

    MEMBERS_CLASS = None
    DATA_CLASS = None
    ITEM_CLASS = None
    ITEM_COLLECTION_CLASS = None

    def __init__(self):
        self._attachments = {}
        self._keys_attachments = {}

    def add_key(self, *keys):
        for key in keys:
            self._keys_attachments[key] = {}
        return self

    def attach(self, name, data, key=None):
        if isinstance(name, str) and isinstance(data, self.DATA_CLASS):  # type: ignore
            if key is not None:
                self._keys_attachments[key][name] = data
            else:
                self._attachments[name] = data
        return self

    def _collect_direct_keys(self, member):
        return dict(
            (k, Attributes.from_nested_dicts(v.get(member))) for k, v in self._attachments.items()
        )

    def _collect_subkeys(self, member):
        attachments = {}
        for key in self._keys_attachments.keys():
            attachments[key] = dict(
                (name, Attributes.from_nested_dicts(data.get(member)))
                for name, data in self._keys_attachments[key].items()
            )
        return Attributes.from_nested_dicts(attachments)

    def collect(self):
        items = []
        for member in self.MEMBERS_CLASS:
            attachments = {}
            if self._attachments:
                attachments.update(self._collect_direct_keys(member))
            if self._keys_attachments:
                attachments.update(self._collect_subkeys(member))
            items.append(self.ITEM_CLASS(member, **attachments))
        return self.ITEM_COLLECTION_CLASS(*items)


class Company(Item):
    """A simple class to handle a company."""

    BASE_CLASS = CoreTypes.Company


class Companies(EnumCollection):
    """A simple class to handle a set of companies."""

    BASE_CLASS = Company


class CompaniesFactory(EnumCollectionFactory):
    """A factory to generate `Companies`."""

    MEMBERS_CLASS = CoreTypes.Company
    DATA_CLASS = CompanyDataMapper
    ITEM_CLASS = Company
    ITEM_COLLECTION_CLASS = Companies


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

    def has_state_religion(self, identifier):
        """Return True if the civilization has the given religion as state religion."""
        return self.state_religion() == identifier

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

    def has_civic(self, id):
        """Return True if the civilization has the civic `id`."""
        return self.player.getCivics(gc.getCivicInfo(id).getCivicOptionType()) == id

    def has_tech(self, id):
        """Return True if the civilization has the tech `id`."""
        return self.team.isHasTech(id)

    def add_tech(self, id, as_first=False, annoncing=False):
        """Add tech `id` to the civilization."""
        self.team.setHasTech(id, True, self.id, as_first, annoncing)

    def remove_tech(self, id):
        """Remove tech `id` to the civilization."""
        self.team.setHasTech(id, False, self.id, False, False)

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


class Civilizations(EnumCollection):
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


class CivilizationsFactory(EnumCollectionFactory):
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
        return player(identifier)

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
        return team(identifier)

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
    return player(identifier).getID() in INDEPENDENT_CIVS


def is_barbarian_civ(identifier):
    """Return True if it's the barbarian."""
    return player(identifier).isBarbarian()


def unittype(identifier):
    if isinstance(identifier, CyUnit):
        return identifier.getUnitType()

    if isinstance(identifier, int):
        return identifier

    raise TypeError("Expected unit type to be CyUnit or int, received: '%s'" % type(identifier))


def base_building(iBuilding):
    if iBuilding is None:
        return iBuilding

    return gc.getBuildingClassInfo(
        gc.getBuildingInfo(iBuilding).getBuildingClassType()
    ).getDefaultBuildingIndex()


def base_unit(iUnit):
    return gc.getUnitClassInfo(
        gc.getUnitInfo(unittype(iUnit)).getUnitClassType()
    ).getDefaultUnitIndex()


def unique_building_from_class(identifier, iBuildingClass):
    return gc.getCivilizationInfo(identifier).getCivilizationBuildings(iBuildingClass)


def unique_building(identifier, iBuilding):
    if not player(identifier):
        return base_building(iBuilding)
    return unique_building_from_class(
        identifier, gc.getBuildingInfo(iBuilding).getBuildingClassType()
    )


def unique_unit_from_class(identifier, iUnitClass):
    return gc.getCivilizationInfo(identifier).getCivilizationUnits(iUnitClass)


def unique_unit(identifier, iUnit):
    if not player(identifier):
        return base_unit(iUnit)
    return unique_unit_from_class(identifier, gc.getUnitInfo(unittype(iUnit)).getUnitClassType())


class Turn(int):
    def __new__(cls, value, *args, **kwargs):
        return super(cls, cls).__new__(cls, value)

    def __add__(self, other):
        return self.__class__(super(Turn, self).__add__(other))

    def __sub__(self, other):
        return self.__class__(super(Turn, self).__sub__(other))

    def between(self, start, end):
        return turn(start) <= self <= turn(end)

    def deviate(self, variation, seed=None):
        variation = turns(variation)
        if seed:
            return self + seed % (2 * variation) - variation
        return self + rand(2 * variation) - variation


def scale(value):
    return turns(value)


def turns(turn):
    if not game.isFinalInitialized():
        return turn

    modifier = Infos().gameSpeed().getGrowthPercent()
    return turn * modifier / 100


def year(year=None):
    if year is None:
        return Turn(gc.getGame().getGameTurn())
    return Turn(getTurnForYear(year))


def turn(turn=None):
    return year(turn)


def until(iTurn):
    return iTurn - turn()


def since(iTurn):
    return turn() - iTurn


class InfoCollection(EntitiesCollection):
    def __init__(self, info_class, *infos):
        super(InfoCollection, self).__init__(*infos)
        self.info_class = info_class

    @classmethod
    def from_type(cls, info_class, n_infos):
        return cls(info_class, *range(n_infos))

    def __str__(self):
        return ",".join([self._factory(i).getText() for i in self])

    def _factory(self, key):
        return self.info_class(key)


class Infos(object):
    def info(self, type):
        return info_types[type][0]

    def of(self, type):
        return info_types[type][1](self)

    def get(self, type, identifier):
        return self.info(type)(self, identifier)

    def text(self, type, identifier):
        return self.get(type, identifier).getText()

    def type(self, string):
        type = gc.getInfoTypeForString(string)
        if type < 0:
            raise ValueError("Type for '%s' does not exist" % string)
        return type

    def constant(self, string):
        return gc.getDefineINT(string)

    def art(self, string):
        return gc.getInterfaceArtInfo(self.type(string)).getPath()

    def attitude(self, identifier):
        return gc.getAttitudeInfo(identifier)

    def attitudes(self):
        return InfoCollection.from_type(gc.getAttitudeInfo, AttitudeTypes.NUM_ATTITUDE_TYPES)

    def bonus(self, identifier):
        if isinstance(identifier, CyPlot):
            return gc.getBonusInfo(identifier.getBonusType(-1))

        if isinstance(identifier, int):
            return gc.getBonusInfo(identifier)

        raise TypeError(
            "Expected identifier to be CyPlot or bonus type ID, got '%s'" % type(identifier)
        )

    def bonuses(self):
        return InfoCollection.from_type(gc.getBonusInfo, gc.getNumBonusInfos())

    def build(self, identifier):
        return gc.getBuildInfo(identifier)

    def builds(self):
        return InfoCollection.from_type(gc.getBuildInfo, gc.getNumBuildInfos())

    def building(self, identifier):
        return gc.getBuildingInfo(identifier)

    def buildings(self):
        return InfoCollection.from_type(gc.getBuildingInfo, gc.getNumBuildingInfos())

    def buildingClass(self, identifier):
        return gc.getBuildingClassInfo(identifier)

    def buildingClasses(self):
        return InfoCollection.from_type(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos())

    def civ(self, identifier):
        if isinstance(identifier, (CyTeam, CyPlayer, CyPlot, CyCity, CyUnit)):
            return gc.getCivilizationInfo(player(identifier).getCivilizationType())

        return gc.getCivilizationInfo(identifier)

    def civs(self):
        return InfoCollection.from_type(gc.getCivilizationInfo, gc.getNumCivilizationInfos())

    def civic(self, identifier):
        return gc.getCivicInfo(identifier)

    def civics(self):
        return InfoCollection.from_type(gc.getCivicInfo, gc.getNumCivicInfos())

    def commerce(self, identifier):
        return gc.getCommerceInfo(identifier)

    def commerces(self):
        return InfoCollection.from_type(gc.getCommerceInfo, CommerceTypes.NUM_COMMERCE_TYPES)

    def corporation(self, identifier):
        return gc.getCorporationInfo(identifier)

    def corporations(self):
        return InfoCollection.from_type(gc.getCorporationInfo, gc.getNumCorporationInfos())

    def cultureLevel(self, identifier):
        return gc.getCultureLevelInfo(identifier)

    def cultureLevels(self):
        return InfoCollection.from_type(gc.getCultureLevelInfo, gc.getNumCultureLevelInfos())

    def era(self, identifier):
        return gc.getEraInfo(identifier)

    def eras(self):
        return InfoCollection.from_type(gc.getEraInfo, gc.getNumEraInfos())

    def feature(self, identifier):
        if isinstance(identifier, CyPlot):
            return gc.getFeatureInfo(identifier.getFeatureType())

        if isinstance(identifier, int):
            return gc.getFeatureInfo(identifier)

        raise TypeError(
            "Expected identifier to be CyPlot or feature type ID, got '%s'" % type(identifier)
        )

    def features(self):
        return InfoCollection.from_type(gc.getFeatureInfo, gc.getNumFeatureInfos())

    def gameSpeed(self, iGameSpeed=None):
        if iGameSpeed is None:
            iGameSpeed = game.getGameSpeedType()
        return gc.getGameSpeedInfo(iGameSpeed)

    def gameSpeeds(self):
        return InfoCollection.from_type(gc.getGameSpeedInfo, gc.getNumGameSpeedInfos())

    def handicap(self, identifier=None):
        if identifier is None:
            identifier = game.getHandicapType()
        return gc.getHandicapInfo(identifier)

    def handicaps(self):
        return InfoCollection.from_type(gc.getHandicapInfo, gc.getNumHandicapInfos())

    def improvement(self, identifier):
        return gc.getImprovementInfo(identifier)

    def improvements(self):
        return InfoCollection.from_type(gc.getImprovementInfo, gc.getNumImprovementInfos())

    def leader(self, identifier):
        if isinstance(identifier, CyPlayer):
            return gc.getLeaderHeadInfo(identifier.getLeader())

        if isinstance(identifier, int):
            return gc.getLeaderHeadInfo(identifier)

        raise TypeError(
            "Expected identifier to be CyPlayer or leaderhead ID, got: '%s'" % type(identifier)
        )

    def leaders(self):
        return InfoCollection.from_type(gc.getLeaderHeadInfo, gc.getNumLeaderHeadInfos())

    def promotion(self, identifier):
        return gc.getPromotionInfo(identifier)

    def promotions(self):
        return InfoCollection.from_type(gc.getPromotionInfo, gc.getNumPromotionInfos())

    def project(self, identifier):
        return gc.getProjectInfo(identifier)

    def projects(self):
        return InfoCollection.from_type(gc.getProjectInfo, gc.getNumProjectInfos())

    def religion(self, iReligion):
        return gc.getReligionInfo(iReligion)

    def religions(self):
        return InfoCollection.from_type(gc.getReligionInfo, gc.getNumReligionInfos())

    def route(self, identifier):
        return gc.getRouteInfo(identifier)

    def routes(self):
        return InfoCollection.from_type(gc.getRouteInfo, gc.getNumRouteInfos())

    def specialist(self, identifier):
        return gc.getSpecialistInfo(identifier)

    def specialists(self):
        return InfoCollection.from_type(gc.getSpecialistInfo, gc.getNumSpecialistInfos())

    def tech(self, identifier):
        return gc.getTechInfo(identifier)

    def techs(self):
        return InfoCollection.from_type(gc.getTechInfo, len(CoreTypes.Technology))

    def terrain(self, identifier):
        return gc.getTerrainInfo(identifier)

    def terrains(self):
        return InfoCollection.from_type(gc.getTerrainInfo, gc.getNumTerrainInfos())

    def unit(self, identifier):
        if isinstance(identifier, CyUnit):
            return gc.getUnitInfo(identifier.getUnitType())

        if isinstance(identifier, int):
            return gc.getUnitInfo(identifier)

        raise TypeError(
            "Expected identifier to be CyUnit or unit type ID, got '%s'" % type(identifier)
        )

    def units(self):
        return InfoCollection.from_type(gc.getUnitInfo, gc.getNumUnitInfos())

    def unitClasses(self):
        return InfoCollection.from_type(gc.getUnitClassInfo, gc.getNumUnitClassInfos())

    def unitCombat(self, identifier):
        return gc.getUnitCombatInfo(identifier)

    def unitCombats(self):
        return InfoCollection.from_type(gc.getUnitCombatInfo, gc.getNumUnitCombatInfos())


try:
    info_types = {
        AttitudeTypes: (Infos.attitude, Infos.attitudes),
        CvBonusInfo: (Infos.bonus, Infos.bonuses),
        CvBuildInfo: (Infos.build, Infos.builds),
        CvBuildingInfo: (Infos.building, Infos.buildings),
        CvBuildingClassInfo: (Infos.buildingClass, Infos.buildingClasses),
        CvCivilizationInfo: (Infos.civ, Infos.civs),
        CvCommerceInfo: (Infos.commerce, Infos.commerces),
        CvCorporationInfo: (Infos.corporation, Infos.corporations),
        CvCultureLevelInfo: (Infos.cultureLevel, Infos.cultureLevels),
        CvEraInfo: (Infos.era, Infos.eras),
        CvFeatureInfo: (Infos.feature, Infos.features),
        CvGameSpeedInfo: (Infos.gameSpeed, Infos.gameSpeeds),
        CvHandicapInfo: (Infos.handicap, Infos.handicaps),
        CvImprovementInfo: (Infos.improvement, Infos.improvements),
        CvLeaderHeadInfo: (Infos.leader, Infos.leaders),
        CvPromotionInfo: (Infos.promotion, Infos.promotions),
        CvProjectInfo: (Infos.project, Infos.projects),
        CvReligionInfo: (Infos.religion, Infos.religions),
        CvRouteInfo: (Infos.route, Infos.routes),
        CvSpecialistInfo: (Infos.specialist, Infos.specialists),
        CvTechInfo: (Infos.tech, Infos.techs),
        CvTerrainInfo: (Infos.terrain, Infos.terrains),
        CvUnitInfo: (Infos.unit, Infos.units),
        UnitCombatTypes: (Infos.unitCombat, Infos.unitCombats),
    }
except:  # noqa: E722
    info_types = {}


class TechCollection(object):
    def __init__(self):
        self._included = []
        self._excluded = []
        self._era = -1
        self._column = 0

    def era(self, era):
        self._era = era
        return self

    def column(self, column):
        self._column = column
        return self

    def without(self, *techs):
        self._excluded += [i for i in techs if i not in self._excluded]
        return self

    def including(self, *techs):
        self._included += [i for i in techs if i not in self._included]
        return self

    def techs(self):
        techs = [
            i
            for i in Infos().techs()
            if Infos().tech(i).getEra() <= self._era or Infos().tech(i).getGridX() <= self._column
        ]
        techs += [i for i in self._included if i not in techs]
        techs = [i for i in techs if i not in self._excluded]
        return techs

    def __iter__(self):
        return iter(self.techs())


class TechFactory(object):
    def none(self):
        return TechCollection()

    def of(self, *techs):
        return TechCollection().including(*techs)

    def era(self, era):
        return TechCollection().era(era)

    def column(self, column):
        return TechCollection().column(column)


def unit(key):
    if isinstance(key, UnitItem):
        return player(key.owner).getUnit(key.id)

    raise TypeError("Expected key to be `Unit`, received '%s'" % type(key))


class UnitItem(object):
    def __init__(self, unit):
        self.owner = unit.getOwner()
        self.id = unit.getID()
        self.x = unit.getX()
        self.y = unit.getY()

    def __eq__(self, other):
        return isinstance(other, UnitItem) and (self.owner, self.id) == (other.owner, other.id)

    def __str__(self):
        return str((self.owner, self.id))

    def __nonzero__(self):
        return self.x >= 0 and self.y >= 0

    @classmethod
    def of(cls, unit):
        if isinstance(unit, cls):
            return unit
        return cls(unit)


class Units(EntitiesCollection):
    def __init__(self, *units):
        super(Units, self).__init__(*[self._keyify(u) for u in units])

    def _keyify(self, item):
        return UnitItem.of(item)

    def _factory(self, key):
        return unit(key)

    def __contains__(self, item):
        if isinstance(item, CyUnit):
            return UnitItem.of(item) in self

        raise TypeError(
            "Tried to check if Units contains '%s', can only contain units" % type(item)
        )

    def __str__(self):
        return ", ".join(
            [
                "%s (%s) at %s"
                % (
                    Infos().unit(unit.getUnitType()).getText(),
                    adjective(unit.getOwner()),
                    (unit.getX(), unit.getY()),
                )
                for unit in self.entities()
            ]
        )

    def owner(self, identifier):
        return self.filter(lambda u: owner(u, identifier))

    def not_owner(self, identifier):
        return self.filter(lambda u: not owner(u, identifier))

    def minor(self):
        return self.filter(lambda u: is_minor_civ(u))

    def type(self, unit_type):
        return self.filter(lambda u: u.getUnitType() == unit_type)

    def by_type(self):
        return dict([(type, self.type(type)) for type in set(self.types())])

    def at_war(self, identifier):
        return self.filter(lambda u: team(identifier).isAtWar(u.getTeam()))

    def domain(self, identifier):
        return self.filter(lambda u: u.getDomainType() == identifier)

    def land(self):
        return self.domain(DomainTypes.DOMAIN_LAND)

    def water(self):
        return self.domain(DomainTypes.DOMAIN_SEA)

    def types(self):
        return [unit.getUnitType() for unit in self]

    def combat(self, combat_type):
        return self.filter(lambda u: u.getUnitCombatType() == combat_type)

    def mercenaries(self):
        return self.filter(lambda u: u.getMercID() > -1)


class UnitFactory:
    def of(self, units):
        return Units(*[UnitItem.of(unit) for unit in units])

    def owner(self, identifier):
        units = iterate(player(identifier).firstUnit, player(identifier).nextUnit, UnitItem.of)
        return Units(*units)

    def at(self, *args):
        if args is None:
            return Units()

        return Units(
            *[UnitItem.of(plot(*args).getUnit(i)) for i in range(plot(*args).getNumUnits())]
        )


class CreatedUnits(object):
    @staticmethod
    def none():
        return CreatedUnits([])

    def __init__(self, units):
        self._units = units

    def __len__(self):
        return len(self._units)

    def __iter__(self):
        return iter(self._units)

    def __add__(self, other):
        return CreatedUnits(self._units + other._units)

    def adjective(self, adjective):
        if not adjective:
            return self

        for unit in self:
            unit.setName("%s %s" % (text(adjective), unit.getName()))

        return self

    def experience(self, experience):
        if experience <= 0:
            return self

        for unit in self:
            unit.changeExperience(experience, 100, False, False, False)

        return self

    def promotion(self, *promotions):
        for promotion in promotions:
            for unit in self:
                unit.setHasPromotion(promotion, True)

        return self

    def one(self):
        if len(self) == 1:
            return self._units[0]
        raise Exception("Can only return one unit if it is a single created unit")

    def count(self):
        return len(self)


def get_player_experience(unit):
    if not unit.canFight():
        return 0

    experience = player(unit).getFreeExperience()
    # experience += player(unit).getDomainFreeExperience(unit.getDomainType())  # TODO

    if player(unit).isStateReligion():
        experience += player(unit).getStateReligionFreeExperience()

    return experience


def _generate_unit(player_id, unit_id, plot, unit_ai, unit_name=None):
    unit_id = int(unit_id)
    x, y = location(plot)
    unit = player(player_id).initUnit(unit_id, x, y, unit_ai, DirectionTypes.DIRECTION_SOUTH)
    unit.changeExperience(get_player_experience(unit), -1, False, False, False)
    unit.testPromotionReady()
    if unit_name is not None:
        unit.setName(unit_name)
    return unit


def make_units(player, unit, plot, n_units=1, unit_ai=None, unit_name=None):
    if unit_ai is None:
        unit_ai = UnitAITypes.NO_UNITAI

    if n_units <= 0:
        return CreatedUnits([])
    if unit < 0:
        raise Exception("Invalid unit")

    units = []
    for _ in range(n_units):
        _unit = _generate_unit(player, unit, plot, unit_ai, unit_name)
        units.append(_unit)
        # events.fireEvent("unitCreated", unit)
    return CreatedUnits(units)


def make_unit(player, unit, plot, unit_ai=None, unit_name=None):
    if unit_ai is None:
        unit_ai = UnitAITypes.NO_UNITAI
    return make_units(player, unit, plot, 1, unit_ai, unit_name).one()


def _generate_crusade_unit(player_id, unit_id, plot, unit_ai, crusade_value):
    # 3Miro: this is a hack to distinguish Crusades without making a separate variable
    unit = _generate_unit(player_id, unit_id, plot, unit_ai)
    unit.setMercID(-5 - crusade_value)
    return unit


def make_crusade_units(player, unit, plot, crusade_value, n_units=1, unit_ai=None):
    if unit_ai is None:
        unit_ai = UnitAITypes.NO_UNITAI
    if n_units <= 0:
        return CreatedUnits([])
    if unit < 0:
        raise Exception("Invalid unit")

    units = []
    for _ in range(n_units):
        _unit = _generate_crusade_unit(player, unit, plot, unit_ai, crusade_value)
        units.append(_unit)
        # events.fireEvent("unitCreated", unit) # TODO
    return CreatedUnits(units)


def make_crusade_unit(player, unit, plot, crusade_value, unit_ai=None):
    if unit_ai is None:
        unit_ai = UnitAITypes.NO_UNITAI
    return make_crusade_units(player, unit, plot, crusade_value, 1, unit_ai).one()


class Locations(EntitiesCollection):
    def __init__(self, *locations):
        super(Locations, self).__init__(*locations)

    def add(self, *addition):
        if not addition or not any(addition):
            return self

        if len(addition) == 1:
            if isinstance(addition[0], Locations):
                total = set(self) + set(addition[0])
                return self.copy(total)

            elif isinstance(addition[0], (list, set)):
                addition = addition[0]

        total = list(set(self)) + list(set(self._keyify(item) for item in addition))
        return self.copy(*total)

    def without(self, *exceptions):
        if not exceptions or not any(exceptions):
            return self

        if len(exceptions) == 1:
            if isinstance(exceptions[0], Locations):
                remaining = set(self) - set(exceptions[0])
                return self.copy(remaining)

            elif isinstance(exceptions[0], (list, set)):
                exceptions = exceptions[0]

        remaining = set(self) - set(self._keyify(item) for item in exceptions)
        return self.copy(*remaining)

    def _closest(self, *args):
        x, y = parse_tile(*args)
        return find_min(self.entities(), lambda loc: distance(loc, (x, y)))

    def closest(self, *args):
        return self._closest(*args).result

    def closest_distance(self, *args):
        return self._closest(*args).value

    def closest_pair(self, locations):
        if not isinstance(locations, Locations):
            raise Exception("Expected instance of Locations, received: %s" % locations)

        permutations = [
            (x, y) for x in self.shuffle().entities() for y in locations.shuffle().entities()
        ]
        return find_min(permutations, lambda x, y: distance(x, y)).result

    def closest_all(self, locations):
        closest = self.closest_pair(locations)
        if closest is None:
            return None

        return closest[0]

    def closest_within(self, *args, **kwargs):
        closest_distance = self.closest_distance(*args)
        radius = kwargs.get("radius", 1)
        if closest_distance is None or closest_distance > radius:
            return self.empty()
        return self.filter(lambda loc: distance(location(*args), loc) == closest_distance)

    def units(self):
        return sum([UnitFactory().at(loc) for loc in self.entities()], Units(*[]))

    def owner(self, identifier):
        return self.filter(lambda loc: owner(loc, identifier))

    def not_owner(self, identifier):
        return self.filter(lambda loc: not owner(loc, identifier))

    def provinces(self, *provinces):
        return self.filter(lambda loc: loc.getProvinceID() in provinces)

    def province(self, identifier):
        return self.provinces(identifier)

    def not_provinces(self, *provinces):
        return self.filter(lambda loc: loc.getProvinceID() not in provinces)

    def not_province(self, identifier):
        return self.not_provinces(identifier)

    def filter_surrounding(self, condition, radius=1):
        return self.filter(
            lambda loc: PlotFactory().surrounding(loc, radius=radius).all(lambda p: condition(p))
        )

    # def owners(self):
    #     return Players(set(loc.getOwner() for loc in self.entities() if loc.getOwner() >= 0)) # TODO

    def areas(self, *areas):
        return self.filter(lambda loc: loc.getArea() in [get_area(area) for area in areas])

    def area(self, area):
        return self.areas(area)

    def intersect(self, locations):
        return any(loc in locations for loc in self)


class Plots(Locations):
    def __init__(self, *plots):
        super(Plots, self).__init__(*[self._keyify(p) for p in plots])

    def _keyify(self, item):
        if isinstance(item, tuple) and len(item) == 2:
            return item

        if isinstance(item, (CyPlot, CyCity, CyUnit)):
            return location(item)

        raise Exception("Not a valid plot key: %s" % type(item))

    def _factory(self, key):
        return plot(key)

    def __contains__(self, item):
        if isinstance(item, (CyPlot, CyCity, CyUnit)):
            return (item.getX(), item.getY()) in self

        if isinstance(item, tuple) and len(item) == 2:
            return item in self

        raise TypeError(
            "Tried to check if Plots contains '%s', can only contain plots, cities, units or coordinate tuples"
            % type(item)
        )

    def cities(self):
        return self.transform(Cities, map=lambda key: city(key), condition=lambda p: p.isCity())

    def land(self):
        return self.filter(lambda p: not p.isWater())

    def water(self):
        return self.filter(lambda p: p.isWater())

    def coastal(self):
        return self.filter(lambda p: p.isCoastalLand())

    def lake(self):
        return self.filter(lambda p: p.isLake())

    def sea(self):
        return self.water().filter(lambda p: not p.isLake())

    # def core(self, identifier):
    #     if isinstance(identifier, Civ):
    #         return self.filter(lambda p: p.isCore(identifier))
    #     return self.filter(lambda p: p.isPlayerCore(identifier))

    def passable(self):
        return self.filter(lambda p: not p.isImpassable())

    def no_enemies(self, identifier):
        return self.filter(lambda p: UnitFactory().at(p).atwar(identifier).none())

    def expand(self, num_tiles):
        return self.enrich(lambda p: PlotFactory().circle(p, radius=num_tiles))

    def edge(self):
        return self.filter(
            lambda p: PlotFactory().surrounding(p).any(lambda sp: sp not in self)
        )  # TODO: check if it's correct


class PlotsCorner:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def end(self, *args):
        x, y = parse_tile(*args)
        return Plots(
            *[
                (i, j)
                for i in range(min(self.x, x), min(max(self.x, x) + 1, WORLD_WIDTH))
                for j in range(min(self.y, y), min(max(self.y, y) + 1, WORLD_HEIGHT))
            ]
        )


class PlotFactory:
    def of(self, list):
        return Plots(*list)

    def start(self, *args):
        x, y = parse_tile(*args)
        return PlotsCorner(x, y)

    def rectangle(self, start, end=None):
        if end is None:
            if isinstance(start, tuple) and len(start) == 2:
                start, end = start
            else:
                raise TypeError(
                    "If only one argument is provided, it needs to be a tuple of two coordinate pairs, got: '%s'"
                    % type(start)
                )
        return self.start(start).end(end)

    def all(self):
        return self.start(0, 0).end(WORLD_WIDTH, WORLD_HEIGHT)

    def none(self):
        return self.of([])

    def provinces(self, *provinces):
        return self.all().filter(lambda p: p.getProvinceID() in provinces)

    def province(self, identifier):
        return self.provinces(identifier)

    def surrounding(self, *args, **kwargs):
        radius = kwargs.get("radius", 1)
        if radius < 0:
            raise ValueError("radius cannot be negative, received: '%d'" % radius)
        x, y = parse_tile(*args)
        if not isinstance(x, int):
            raise Exception("x must be int, is %s" % type(x))
        if not isinstance(y, int):
            raise Exception("y must be int, is %s" % type(y))
        return Plots(
            *sort(
                list(
                    set(
                        wrap(x + i, y + j)
                        for i in range(-radius, radius + 1)
                        for j in range(-radius, radius + 1)
                    )
                )
            )
        )

    def ring(self, *args, **kwargs):
        radius = kwargs.get("radius", 1)
        circle = self.surrounding(*args, **kwargs)
        inside = self.surrounding(*args, **{"radius": radius - 1})
        return circle.without(inside)

    def circle(self, *args, **kwargs):
        radius = kwargs.get("radius", 1)
        square = self.surrounding(*args, **kwargs)
        x, y = parse_tile(*args)
        return square.filter(lambda p: plotDistance(p.getX(), p.getY(), x, y) <= radius)

    def city_radius(self, city):
        if not city or city.isNone():
            raise TypeError("city object is None")

        return Plots(*[location(city.getCityIndexPlot(i)) for i in range(21)])

    def owner(self, identifier):
        return self.all().owner(identifier)

    # def area(self, dArea, dExceptions, identifier):
    #     return (
    #         self.rectangle(*dArea[identifier])
    #         .without(dExceptions[identifier])
    #         .clear_named(infos.civ(identifier).getShortDescription(0))
    #     )

    def sum(self, areas):
        return sum(areas, self.none())

    # def birth(self, identifier, extended=None):
    #     if extended is None:
    #         extended = isExtendedBirth(identifier)
    #     if identifier in dExtendedBirthArea and extended:
    #         return self.area(dExtendedBirthArea, dBirthAreaExceptions, identifier)
    #     return self.area(dBirthArea, dBirthAreaExceptions, identifier)

    # def core(self, identifier):
    #     iPeriod = player(identifier).getPeriod()
    #     if iPeriod in dPeriodCoreArea:
    #         return self.area(dPeriodCoreArea, dPeriodCoreAreaExceptions, iPeriod)
    #     return self.area(dCoreArea, dCoreAreaExceptions, identifier)

    # def normal(self, identifier):
    #     iPeriod = player(identifier).getPeriod()
    #     if iPeriod in dPeriodNormalArea:
    #         return self.area(dPeriodNormalArea, dPeriodNormalAreaExceptions, iPeriod)
    #     return self.area(dNormalArea, dNormalAreaExceptions, identifier)

    # def broader(self, identifier):
    #     iPeriod = player(identifier).getPeriod()
    #     if iPeriod in dPeriodBroaderArea:
    #         return self.rectangle(*dPeriodBroaderArea[identifier])
    #     return self.rectangle(*dBroaderArea[identifier])

    # def expansion(self, identifier):
    #     if identifier not in dExpansionArea:
    #         return self.none()
    #     return self.area(dExpansionArea, dExpansionAreaExceptions, identifier)

    # def respawn(self, identifier):
    #     if identifier in dRespawnArea:
    #         return self.rectangle(*dRespawnArea[identifier])
    #     return self.normal(identifier)

    # def capital(self, identifier):
    #     iPeriod = player(identifier).getPeriod()
    #     if iPeriod in dPeriodCapitals:
    #         return plot(dPeriodCapitals[iPeriod])
    #     return plot(dCapitals[identifier])

    # def capitals(self, identifier):
    #     return self.of([self.capital(identifier)])

    # def respawnCapital(self, identifier):
    #     if identifier in dRespawnCapitals:
    #         return plot(dRespawnCapitals[identifier])
    #     return self.capital(identifier)

    # def newCapital(self, identifier):
    #     if identifier in dNewCapitals:
    #         return plot(dNewCapitals[identifier])
    #     return self.respawnCapital(identifier)


class CityItem(object):
    def __init__(self, city):
        self.owner = city.getOwner()
        self.id = city.getID()

    def __eq__(self, other):
        return isinstance(other, CityItem) and (self.owner, self.id) == (other.owner, other.id)

    def __str__(self):
        return str((self.owner, self.id))

    @classmethod
    def of(cls, city):
        if isinstance(city, cls):
            return city
        return cls(city)


class Cities(Locations):
    def __init__(self, *cities):
        super(Cities, self).__init__(*[self._keyify(city) for city in cities])

    def _keyify(self, item):
        return CityItem.of(item)

    def _factory(self, key):
        if isinstance(key, CityItem):
            return player(key.owner).getCity(key.id)

        raise TypeError("Can only use keys of type CityKey in Cities, got: %s" % type(key))

    def __contains__(self, item):
        if isinstance(item, (CyCity, CityItem)):
            return CityItem.of(item) in self

        elif isinstance(item, CyPlot):
            if not item.isCity():
                return False
            return self.__contains__(item.getPlotCity())

        elif isinstance(item, CyUnit):
            return self.__contains__(item.plot())

        elif isinstance(item, tuple) and len(item) == 2:
            return self.__contains__(plot(item))

        raise TypeError(
            "Tried to check if Cities contains '%s', can only contain plots, cities, units or coordinate tuples"
            % type(item)
        )

    def __str__(self):
        return str(
            [
                "%s (%s) at %s"
                % (city.getName(), adjective(city.getOwner()), (city.getX(), city.getY()))
                for city in self.entities()
            ]
        )

    def without(self, *exceptions):
        if not exceptions or none(exceptions):
            return self

        if len(exceptions) == 1 and isinstance(exceptions[0], (list, set, Locations)):
            exceptions = exceptions[0]

        return self.filter(
            lambda city: location(city) not in [location(loc) for loc in exceptions]
        )

    def existing(self):
        return self.filter(lambda city: city.getX() >= 0)

    def religion(self, identifier):
        return self.filter(lambda city: city.isHasReligion(identifier))

    def not_religion(self, identifier):
        return self.filter(lambda city: not city.isHasReligion(identifier))

    def corporation(self, identifier):
        return self.filter(lambda city: city.isHasCorporation(identifier))

    def not_corporation(self, identifier):
        return self.filter(lambda city: not city.isHasCorporation(identifier))

    def building(self, identifier):
        return self.filter(lambda city: city.isHasRealBuilding(identifier))

    def not_building(self, identifier):
        return self.filter(lambda city: not city.isHasRealBuilding(identifier))

    def building_effect(self, identifier):
        return self.filter(lambda city: city.isHasBuildingEffect(identifier))

    def not_building_effect(self, identifier):
        return self.filter(lambda city: not city.isHasBuildingEffect(identifier))

    def coastal(self, value=10):
        return self.filter(lambda city: city.isCoastal(value))

    # def core(self, identifier):
    #     if isinstance(identifier, Civ):
    #         return self.filter(lambda city: city.isCore(identifier))
    #     return self.filter(lambda city: city.isPlayerCore(identifier))

    def plots(self):
        return self.transform(Plots, map=lambda key: plot(self._factory(key)))


class CitiesCorner:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def end(self, *args):
        x, y = parse_tile(*args)
        return PlotsCorner(self.x, self.y).end(x, y).cities()


class CityFactory:
    def __init__(self):
        self.plots = PlotFactory()

    def owner(self, identifier):
        owner = player(identifier)
        cities = iterate(owner.firstCity, owner.nextCity)
        return Cities(*cities)

    def main(self):  # TODO apply this on location and in plot factory, may need the switch to _key
        return self.all().filter(lambda loc: is_main_civ(loc))

    def majors(self):
        return self.all().filter(lambda loc: is_major_civ(loc))

    def minors(self):
        return self.all().filter(lambda loc: is_minor_civ(loc))

    def barbarian(self):
        return self.all().filter(lambda loc: is_barbarian_civ(loc))

    def all(self):
        cities = []
        for player_id in range(gc.getMAX_PLAYERS()):  # TODO
            if player(player_id).getCivilizationType() >= 0:
                cities += self.owner(player_id)
        return Cities(*cities)

    def start(self, *args):
        x, y = parse_tile(*args)
        return CitiesCorner(x, y)

    def rectangle(self, start, end=None):
        if end is None:
            if isinstance(start, tuple) and len(start) == 2:
                start, end = start
            else:
                raise TypeError(
                    "If only one argument is provided, it needs to be a tuple of two coordinate pairs, got: '%s'"
                    % type(start)
                )
        return self.start(start).end(end)

    def provinces(self, *provinces):
        return self.plots.provinces(*provinces).cities()

    def province(self, identifier):
        return self.provinces(identifier)

    def of(self, list):
        return self.plots.of(list).cities()

    def none(self):
        return self.of([])

    def ids(self, identifier, ids):
        return Cities(*[player(identifier).getCity(id) for id in ids])

    def surrounding(self, *args, **kwargs):
        return self.plots.surrounding(*args, **kwargs).cities()

    def ring(self, *args, **kwargs):
        return self.plots.ring(*args, **kwargs).cities()

    # def birth(self, identifier, extended=None):
    #     return self.plots.birth(identifier, extended).cities()

    # def core(self, identifier):
    #     return self.plots.core(identifier).cities()

    # def normal(self, identifier):
    #     return self.plots.normal(identifier).cities()

    # def broader(self, identifier):
    #     return self.plots.broader(identifier).cities()

    # def respawn(self, identifier):
    #     return self.plots.respawn(identifier).cities()

    # def capital(self, identifier):
    #     return city(self.plots.capital(identifier))

    # def respawnCapital(self, identifier):
    #     return city(self.plots.respawnCapital(identifier))

    # def newCapital(self, identifier):
    #     return city(self.plots.newCapital(identifier))


def owner(entity, identifier):
    return entity.getOwner() == identifier


def wrap(*args):
    parsed = parse_tile(*args)
    if parsed is None:
        return None
    x, y = parsed
    return x % WORLD_WIDTH, max(0, min(y, WORLD_HEIGHT - 1))


def iterate(first, next, getter=lambda x: x):
    list = []
    entity, iter = first(False)
    while entity:
        list.append(getter(entity))
        entity, iter = next(iter, False)
    return [x for x in list if x is not None]


def plot(*args):
    x, y = parse_tile(*args)
    return gc.getMap().plot(x, y)


def city(*args):
    if len(args) == 1 and isinstance(args[0], CyCity):
        return args[0]

    p = plot(*args)
    if not p.isCity():
        return None
    return p.getPlotCity()


def location(entity):
    if not entity:
        return None

    if isinstance(entity, (CyPlot, CyCity, CyUnit)):
        return entity.getX(), entity.getY()

    return parse_tile(entity)


def parse_tile(*args):
    if len(args) == 2:
        return args
    elif len(args) == 1:
        if isinstance(args[0], tuple) and len(args[0]) == 2:
            return args[0]
        elif isinstance(args[0], (CyPlot, CyCity, CyUnit)):
            if args[0].isNone() or args[0].getX() < 0 or args[0].getY() < 0:
                return None
            return args[0].getX(), args[0].getY()

    raise TypeError(
        "Only accepts two coordinates or a tuple of two coordinates, received: %s %s"
        % (args, type(args[0]))
    )


def get_area(area):
    if isinstance(area, (CyPlot, CyCity)):
        return area.getArea()
    elif isinstance(area, CyUnit):
        return get_area(plot(area))
    elif isinstance(area, tuple) and len(area) == 2:
        return plot(area).getArea()
    return area


def distance(location1, location2):
    if not location1 or not location2:
        return map.maxStepDistance()

    x1, y1 = parse_tile(location1)
    x2, y2 = parse_tile(location2)
    return stepDistance(x1, y1, x2, y2)


def closest_city(entity, owner=None, same_continent=False, coastal_only=False, skip_city=None):
    if owner is None:
        owner = PlayerTypes.NO_PLAYER

    if skip_city is None:
        if isinstance(entity, CyCity):
            skip_city = entity
        else:
            skip_city = CyCity()
    elif isinstance(skip_city, CyPlot):
        skip_city = skip_city.isCity() and city(skip_city) or CyCity()

    x, y = parse_tile(entity)
    city_ = map.findCity(
        x,
        y,
        owner,
        TeamTypes.NO_TEAM,
        same_continent,
        coastal_only,
        TeamTypes.NO_TEAM,
        DirectionTypes.NO_DIRECTION,
        skip_city,
    )

    if city_.isNone():
        return None
    return city_


class FindResult(object):
    def __init__(self, result, index, value):
        self.result = result
        self.index = index
        self.value = value


def find(list, metric=lambda x: x, reverse=True):
    if not list:
        return FindResult(None, None, None)
    result = sort(list, metric, reverse)[0]
    return FindResult(result=result, index=list.index(result), value=metric(result))


def find_min(list, metric=lambda x: x):
    return find(list, metric, False)


def find_max(list, metric=lambda x: x):
    return find(list, metric, True)


def text(key, *format):
    return translator.getText(str(key), tuple(format))


def text_if_exists(key, *format, **kwargs):
    otherwise = kwargs.get("otherwise")
    key_text = text(key, *format)
    if key_text != key:
        return key_text
    elif otherwise:
        return text(otherwise, *format)
    return ""


def colortext(key, color, *format):
    return translator.getColorText(str(key), tuple(format), gc.getInfoTypeForString(color))


def font_text(text, fontsize=2):
    return u"<font=%s>%s</font>" % (str(fontsize), text)


def symbol(identifier):
    return unichr(CyGame().getSymbolID(identifier))  # noqa: F821


def font_symbol(iSymbol, fontsize=2):
    return font_text(symbol(iSymbol), fontsize)


def show_if_human(player, message, *format):
    if human() == player:
        show(message, *format)


def show(message, *format):
    if format:
        message = message % tuple(format)

    popup = Popup.PyPopup()
    popup.setBodyString(message)
    popup.launch()


def event_popup(id, title, message, labels=None):
    if labels is None:
        labels = []

    popup = Popup.PyPopup(id, EventContextTypes.EVENTCONTEXT_ALL)
    popup.setHeaderString(title)
    popup.setBodyString(message)
    for label in labels:
        popup.addButton(label)
    popup.launch(not labels)


def message_if_human(player, text, **settings):
    if human() == player:
        message(player, text, **settings)


def message(player, text, **settings):
    force = settings.get("force", False)
    duration = settings.get("duration", MessageData.DURATION)
    sound = settings.get("sound", "")
    event = settings.get("event", 0)
    button = settings.get("button", "")
    color = settings.get("color", MessageData.WHITE)

    tile = settings.get("location")
    x, y = -1, -1
    if tile:
        x, y = location(tile)

    interface.addMessage(
        int(player),
        force,
        duration,
        text,
        sound,
        event,
        button,
        ColorTypes(color),
        x,
        y,
        True,
        True,
    )


def get_data_from_province_map(plot):
    x, y = location(plot)
    return PROVINCES_MAP[y][x]


def get_data_from_upside_down_map(map, civ, plot):
    x, y = location(plot)
    return map[civ][WORLD_HEIGHT - 1 - y][x]


def get_scenario():
    """Return scenario given the current situation."""
    try:
        if player(Civ.BURGUNDY).isPlayable():
            return Scenario.i500AD
    except:  # noqa: E722
        return Scenario.i1200AD
    else:
        return Scenario.i1200AD


def get_scenario_start_years(scenario=None):
    """Return scenario start year given a scenario."""
    if scenario is None:
        scenario = get_scenario()

    years = [500, 1200]
    return years[scenario]


def get_scenario_start_turn(scenario=None):
    """Return scenario start turn given a scenario."""
    if scenario is None:
        scenario = get_scenario()

    dateturn = [year(500), year(1200)]
    return dateturn[scenario]


def civilizations(scenario=None):
    """Return civilizations data given a scenario."""
    if scenario is None:
        scenario = get_scenario()

    data_mapper = {Scenario.i500AD: civilizations_500AD, Scenario.i1200AD: civilizations_1200AD}
    return data_mapper[scenario]


def civilization(identifier=None):
    """Return Civilization object given an identifier."""
    if identifier is None:
        return civilizations()[gc.getGame().getActiveCivilizationType()]

    if isinstance(identifier, int):
        return civilizations()[identifier]

    if isinstance(identifier, Civ):
        return civilizations()[identifier]

    if isinstance(identifier, Civilization):
        return civilizations()[identifier.id]

    if isinstance(identifier, (CyPlayer, CyUnit)):
        return civilizations()[identifier.getCivilizationType()]

    if isinstance(identifier, CyPlot):
        if not identifier.isOwned():
            return None
        return civilizations()[identifier.getOwner()]

    if isinstance(identifier, CyCity):
        return civilizations()[identifier.getOwner()]

    raise NotTypeExpectedError(
        "CoreTypes.Civ, Civilization, CyPlayer, CyPlot, CyCity or CyUnit, or int", type(identifier)
    )


companies = (
    CompaniesFactory()
    .attach("birthdate", COMPANY_BIRTHDATE)
    .attach("deathdate", COMPANY_DEATHDATE)
    .attach("region", COMPANY_REGION)
    .attach("limit", COMPANY_LIMIT)
    .collect()
)
civilizations_base = (
    CivilizationsFactory()
    .add_key("initial", "location", "religion", "human", "ai", "misc", "date", "event", "scenario")
    .attach("leaders", CIV_LEADERS)
    .attach("respawning_threshold", CIV_RESPAWNING_THRESHOLD, key="location")
    .attach("capital", CIV_CAPITAL_LOCATIONS, key="location")
    .attach("new_capital", CIV_NEW_CAPITAL_LOCATIONS, key="location")
    .attach("neighbours", CIV_NEIGHBOURS, key="location")
    .attach("reformation_neighbours", CIV_REFORMATION_NEIGHBOURS, key="location")
    .attach("home_colony", CIV_HOME_LOCATIONS, key="location")
    .attach("provinces", CIV_PROVINCES, key="location")
    .attach("area", CIV_AREAS, key="location")
    .attach("spreading_threshold", CIV_RELIGION_SPREADING_THRESHOLD, key="religion")
    .attach("tolerance", CIV_RELIGIOUS_TOLERANCE, key="religion")
    .attach("modifiers", CIV_HUMAN_MODIFIERS, key="human")
    .attach("modifiers", CIV_AI_MODIFIERS, key="ai")
    .attach("stop_birth_threshold", CIV_AI_STOP_BIRTH_THRESHOLD, key="ai")
    .attach("stability_bonus", CIV_STABILITY_AI_BONUS, key="ai")
    .attach("reformation_threshold", CIV_AI_REFORMATION_THRESHOLD, key="ai")
    .attach("hire_mercenary_threshold", CIV_HIRE_MERCENARY_THRESHOLD, key="misc")
    .attach("birth", CIV_BIRTHDATE, key="date")
    .attach("collapse", CIV_COLLAPSE_DATE, key="date")
    .attach("respawning", CIV_RESPAWNING_DATE, key="date")
    .attach("buildings", CIV_INITIAL_BUILDINGS, key="initial")
    .attach("tech", CIV_INITIAL_TECH, key="initial")
    .attach("workers", CIV_INITIAL_WORKERS, key="initial")
    .attach("units", CIV_INITIAL_UNITS, key="initial")
    .attach("additional_units", CIV_ADDITIONAL_UNITS, key="initial")
    .attach("provinces", CIV_EVENT_DRIVE_PROVINCES, key="event")
)
civilizations_500AD = (
    civilizations_base.attach("visible_area", CIV_VISIBLE_AREA[Scenario.i500AD], key="location")
    .attach("condition", CIV_SCENARIO_CONDITION[Scenario.i500AD], key="scenario")
    .attach("contact", CIV_INITIAL_CONTACTS[Scenario.i500AD], key="scenario")
    .attach("wars", CIV_INITIAL_WARS[Scenario.i500AD], key="scenario")
    .collect()
)
civilizations_1200AD = (
    civilizations_base.attach("visible_area", CIV_VISIBLE_AREA[Scenario.i1200AD], key="location")
    .attach("condition", CIV_SCENARIO_CONDITION[Scenario.i1200AD], key="scenario")
    .attach("contact", CIV_INITIAL_CONTACTS[Scenario.i1200AD], key="scenario")
    .attach("wars", CIV_INITIAL_WARS[Scenario.i1200AD], key="scenario")
    .collect()
)

techs = TechFactory
units = UnitFactory
plots = PlotFactory
cities = CityFactory
infos = Infos
