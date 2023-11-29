import CoreTypes
from Consts import WORLD_HEIGHT, WORLD_WIDTH

try:
    from CvPythonExtensions import CyGlobalContext, CyPlot, CyCity, CyUnit, stepDistance

    gc = CyGlobalContext()
    map = gc.getMap()

except ImportError:
    gc = None
    map = None


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


def _iterate(first, next, getter=lambda x: x):
    list = []
    entity, iter = first(False)
    while entity:
        list.append(getter(entity))
        entity, iter = next(iter, False)
    return [x for x in list if x is not None]


def _parse_tile(*args):
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
    parsed = _parse_tile(*args)
    if parsed is None:
        return None
    x, y = parsed
    return x % WORLD_WIDTH, max(0, min(y, WORLD_HEIGHT - 1))


def plot(*args):
    x, y = _parse_tile(*args)
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

    return _parse_tile(entity)


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

    x1, y1 = _parse_tile(location1)
    x2, y2 = _parse_tile(location2)
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
