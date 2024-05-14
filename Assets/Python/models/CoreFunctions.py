import CoreTypes
from Consts import WORLD_HEIGHT, WORLD_WIDTH, MessageData
from ProvinceMapData import PROVINCES_MAP

try:
    from CvPythonExtensions import (
        CyGlobalContext,
        CyTranslator,
        CyInterface,
        CyPlot,
        CyCity,
        CyUnit,
        stepDistance,
        EventContextTypes,
        ColorTypes,
        PlayerTypes,
        TeamTypes,
        DirectionTypes,
        CyGame,
    )
    import Popup

    gc = CyGlobalContext()
    map = gc.getMap()
    translator = CyTranslator()
    interface = CyInterface()

except ImportError:
    gc = None
    map = None
    translator = None
    interface = None


def get_enum_by_id(enum, id):
    """Return a enum member by its index."""
    return enum[enum._member_names_[id]]


def get_civ_by_id(id):
    """Return a Civ member by its index."""
    return get_enum_by_id(CoreTypes.Civ, id)


def get_religion_by_id(id):
    """Return a Religion member by its index."""
    return get_enum_by_id(CoreTypes.Religion, id)


def religion(identifier):
    """Return the identifier of a religion."""
    if isinstance(identifier, int):
        return identifier

    if isinstance(identifier, CoreTypes.Religion):
        return identifier.value


def parse_area_dict(data):
    """Parse a dict of area properties."""
    return {
        CoreTypes.Area.TILE_MIN: data[CoreTypes.Area.TILE_MIN],
        CoreTypes.Area.TILE_MAX: data[CoreTypes.Area.TILE_MAX],
        CoreTypes.Area.ADDITIONAL_TILES: data.get(CoreTypes.Area.ADDITIONAL_TILES, []),
        CoreTypes.Area.EXCEPTION_TILES: data.get(CoreTypes.Area.EXCEPTION_TILES, []),
    }


def iterate(first, next, getter=lambda x: x):
    list = []
    entity, iter = first(False)
    while entity:
        list.append(getter(entity))
        entity, iter = next(iter, False)
    return [x for x in list if x is not None]


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


def wrap(*args):
    parsed = parse_tile(*args)
    if parsed is None:
        return None
    x, y = parsed
    return x % WORLD_WIDTH, max(0, min(y, WORLD_HEIGHT - 1))


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


def owner(entity, identifier):
    return entity.getOwner() == identifier


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


def sort(iterable, key=lambda x: x, reverse=False):
    return sorted(iterable, key=key, reverse=reverse)


def find_max(list, metric=lambda x: x):
    return find(list, metric, True)


def find_min(list, metric=lambda x: x):
    return find(list, metric, False)


def find(list, metric=lambda x: x, reverse=True):
    if not list:
        return FindResult(None, None, None)
    result = sort(list, metric, reverse)[0]
    return FindResult(result=result, index=list.index(result), value=metric(result))


class FindResult(object):
    def __init__(self, result, index, value):
        self.result = result
        self.index = index
        self.value = value


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


def small_text(text, fontsize=2):
    return u"<font=%i>%s</font>" % (fontsize, text)


def symbol(identifier):
    return unichr(CyGame().getSymbolID(identifier))  # noqa: F821


def small_symbol(iSymbol, fontsize=2):
    return small_text(symbol(iSymbol), fontsize)


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
    return map[get_civ_by_id(civ)][WORLD_HEIGHT - 1 - y][x]
