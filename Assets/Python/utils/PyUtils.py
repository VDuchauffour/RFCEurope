import operator
from random import randint


def all(iterable):
    """Return True if all elements of the iterable are true (or if the iterable is empty)."""
    for element in iterable:
        if not element:
            return False
    return True


def any(iterable):
    """Return True if any element of the iterable is true. If the iterable is empty, return False."""
    for element in iterable:
        if element:
            return True
    return False


def partial(func, *args, **keywords):
    """Return a new partial object which when called will behave like func called with the positional arguments args and keyword arguments keywords."""

    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*(args + fargs), **newkeywords)

    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc


def product(repeat=1, *args):
    """Cartesian product of input iterables.

    Equivalent to product(repeat=1, 'ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    or product(repeat=3, range(2)) --> 000 001 010 011 100 101 110 111
    """
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x + [y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


def permutations(iterable, r=None):
    """Return successive r length permutations of elements in the iterable.

    Equivalent to permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    or permutations(range(3)) --> 012 021 102 120 201 210
    """
    pool = tuple(iterable)
    n = len(pool)
    if r is None:
        r = n
    for indices in product(r, range(n)):
        if len(set(indices)) == r:
            yield tuple(pool[i] for i in indices)


def combinations(iterable, r):
    """Return r length subsequences of elements from the input iterable.

    Equivalent to combinations('ABCD', 2) --> AB AC AD BC BD CD
    or combinations(range(4), 3) --> 012 013 023 123
    """
    pool = tuple(iterable)
    n = len(pool)
    for indices in permutations(range(n), r):
        if sorted(indices) == list(indices):
            yield tuple(pool[i] for i in indices)


def rand(left, right=None):
    """Return a random number between two ones."""
    if right is None:
        right = left
        left = 0
    return randint(left, right)


def chance(threshold, percentage, strict=False):
    """Return True if a random number between 0 and `threshold` is less than or equal to `percentage`. If `strict` is True the chosen operator is less than."""
    if not 0 <= percentage <= threshold or not isinstance(percentage, int):
        raise ValueError("`percentage` must an int, received %s" % percentage)
    if strict:
        op = operator.__le__
    else:
        op = operator.__lt__
    return op(rand(threshold), percentage)


percentage_chance = partial(chance, 100)


def resolve_attr(obj, attr):
    for name in attr.split("."):
        obj = getattr(obj, name)
    return obj


def attrgetter(*items):
    """Return a callable object that fetches attr from its operand. If more than one attribute is requested, returns a tuple of attributes.
    The attribute names can also contain dots."""
    if len(items) == 1:
        attr = items[0]

        def g(obj):
            return resolve_attr(obj, attr)

    else:

        def g(obj):
            return tuple(resolve_attr(obj, attr) for attr in items)

    return g
