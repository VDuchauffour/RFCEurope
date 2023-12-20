from bisect import bisect
from itertools import repeat
import operator
from random import random
from random import choice as _choice

from Errors import NotTypeExpectedError

try:
    from CvPythonExtensions import CyGlobalContext

    gc = CyGlobalContext()

except ImportError:
    gc = None


def all(iterable):
    """Return True if all elements of the iterable are true (or if the iterable is empty)."""  # type: ignore
    for element in iterable:
        if not element:
            return False
    return True


def any(iterable):
    """Return True if any element of the iterable is true. If the iterable is empty, return False."""  # type: ignore
    for element in iterable:
        if element:
            return True
    return False


def none(iterable):
    """Return True if not any element of the iterable is true."""
    return not any(iterable)


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


def accumulate(iterable, func=operator.add):
    """Return running totals.

    Equivalent to accumulate([1,2,3,4,5]) --> 1 3 6 10 15
    or accumulate([1,2,3,4,5], initial=100) --> 100 101 103 106 110 115
    or accumulate([1,2,3,4,5], operator.mul) --> 1 2 6 24 120
    """
    it = iter(iterable)
    total = 0
    for element in it:
        total = func(total, element)
        yield total


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
    return left + gc.getGame().getSorenRandNum(right - left, "random number")


def percentage():
    """Return a random number between 0 and 99."""
    return rand(100)


def choices(population, weights=None, cum_weights=None, k=1):
    """Return a k sized list of population elements chosen with replacement.

    If the relative weights or cumulative weights are not specified,
    the selections are made with equal probability.
    """
    n = len(population)
    if cum_weights is None:
        if weights is None:
            return [_choice(population) for i in repeat(None, k)]
        try:
            cum_weights = list(accumulate(weights))
        except TypeError:
            if not isinstance(weights, int):
                raise
            k = weights
            raise TypeError("The number of choices must be a keyword argument: k=%s" % k)
    elif weights is not None:
        raise TypeError("Cannot specify both weights and cumulative weights")
    if len(cum_weights) != n:
        raise ValueError("The number of weights does not match the population")
    total = cum_weights[-1] + 0.0  # convert to float
    if total <= 0.0:
        raise ValueError("Total of weights must be greater than zero")
    hi = n - 1
    return [population[bisect(cum_weights, random() * total, 0, hi)] for i in repeat(None, k)]


def choice(population, weights=None, cum_weights=None):
    """Return a single item of population elements chosen with replacement.

    If the relative weights or cumulative weights are not specified,
    the selections are made with equal probability.
    """
    return choices(population, weights, cum_weights)[0]


def random_entry(iterable):
    """Return a single item of population elements chosen with replacement.

    Return None if the iterable is empty.
    """
    if not iterable:
        return None

    return choice(iterable)


def chance(threshold, percentage, strict=False, reverse=False):
    """Return True if a random number is between 0 and `threshold` is less than or equal to `percentage`.
    If `strict` is True the chosen operator is less than. If `reverse` is True, the comparison
    order is reversed.
    """
    if not isinstance(percentage, int):
        raise NotTypeExpectedError(int, type(percentage))

    if reverse:
        if strict:
            op = operator.__gt__
        else:
            op = operator.__ge__
    else:
        if strict:
            op = operator.__lt__
        else:
            op = operator.__le__
    return op(rand(threshold), percentage)


def percentage_chance(percentage, strict=False, reverse=False):
    """Return True if a random number is between 0 and 100 is less than or equal to `percentage`.
    If `strict` is True the chosen operator is less than. If `reverse` is True, the comparison
    order is reversed.
    """
    return chance(100, percentage, strict, reverse)


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
