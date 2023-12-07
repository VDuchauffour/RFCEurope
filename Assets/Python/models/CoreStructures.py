from Consts import INDEPENDENT_CIVS
from CoreFunctions import get_civ_by_id, iterate, location, owner, plot, religion, text
from PyUtils import any, rand
import CoreTypes
from BaseStructures import (
    EntitiesCollection,
    EnumCollectionFactory,
    Collection,
    EnumDataMapper,
    Item,
    EnumCollection,
)
from Errors import NotTypeExpectedError

try:
    from CvPythonExtensions import (
        CyGlobalContext,
        CyPlayer,
        CyTeam,
        CyPlot,
        CyCity,
        CyUnit,
        AttitudeTypes,
        CommerceTypes,
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
        DomainTypes,
        UnitAITypes,
        DirectionTypes,
    )

    gc = CyGlobalContext()
    game = gc.getGame()

except ImportError:
    gc = None
    game = None


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


class Companies(EnumCollection):
    """A simple class to handle a set of companies."""

    BASE_CLASS = Company


class CompaniesFactory(EnumCollectionFactory):
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

    def has_state_religion(self, identifier):
        """Return True if the civilization has the given religion as state religion."""
        return self.state_religion() == religion(identifier)

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
    return get_civ_by_id(player(identifier).getID()) in INDEPENDENT_CIVS


def is_barbarian_civ(identifier):
    """Return True if it's the barbarian."""
    return player(identifier).isBarbarian()


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

    modifier = infos.gameSpeed().getGrowthPercent()
    return turn * modifier / 100


def year(year=None):
    if year is None:
        return Turn(gc.getGame().getGameTurn())
    return Turn(getTurnForYear(year))


def turn(turn=None):
    return year(turn)


class InfoCollection(Collection):
    def __init__(self, info_class, *infos):
        super(InfoCollection, self).__init__(*infos)
        self.info_class = info_class

    @classmethod
    def from_type(cls, info_class, n_infos):
        return cls(info_class, *range(n_infos))

    def __str__(self):
        return ",".join([self.info_class(i).getText() for i in self])


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
            for i in infos.techs()
            if infos.tech(i).getEra() <= self._era or infos.tech(i).getGridX() <= self._column
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
        super(Units, self).__init__(*[UnitItem.of(u) for u in units])

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
                    infos.unit(unit.getUnitType()).getText(),
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


def make_units(player, unit, plot, n_units=1, unit_ai=UnitAITypes.NO_UNITAI, unit_name=None):
    if n_units <= 0:
        return CreatedUnits([])
    if unit < 0:
        raise Exception("Invalid unit")

    units = []
    for _ in range(n_units):
        _unit = _generate_unit(player, unit, plot, unit_ai, unit_name)
        units.append(_unit)
        # events.fireEvent("unitCreated", unit) # TODO
    return CreatedUnits(units)


def make_unit(player, unit, plot, unit_ai=UnitAITypes.NO_UNITAI, unit_name=None):
    return make_units(player, unit, plot, 1, unit_ai, unit_name).one()


def _generate_crusade_unit(player_id, unit_id, plot, unit_ai, crusade_value):
    # 3Miro: this is a hack to distinguish Crusades without making a separate variable
    unit = _generate_unit(player_id, unit_id, plot, unit_ai)
    unit.setMercID(-5 - crusade_value)
    return unit


def make_crusade_units(
    player, unit, plot, crusade_value, n_units=1, unit_ai=UnitAITypes.NO_UNITAI
):
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


def make_crusade_unit(player, unit, plot, crusade_value, unit_ai=UnitAITypes.NO_UNITAI):
    return make_crusade_units(player, unit, plot, crusade_value, 1, unit_ai).one()


infos = Infos()
