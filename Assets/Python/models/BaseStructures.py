from itertools import groupby
import random
from copy import copy, deepcopy
from CoreFunctions import sort
import CoreTypes

from Enum import Enum, IntEnum
from Errors import NotACallableError, NotTypeExpectedError, OutputTypeError
from PyUtils import (
    all,
    any,
    attrgetter,
    choices,
    combinations,
    permutations,
    product,
    random_entry,
)


class OutputType(Enum):
    SINGLE = 0
    MULTIPLE = 1


class DataMapper(dict):
    """Base class to map data to a specific data type."""

    BASE_CLASS = int

    def __init__(self, elements, default=None):
        self._default = default
        for key, value in elements.items():
            self[key] = value

    def _check_condition(self, key):
        return isinstance(key, self.BASE_CLASS)

    def __contains__(self, key):
        if self._check_condition(key):
            return dict.__contains__(self, key)
        raise TypeError(
            "%s only accepts keys of type %s, received: %s"
            % (self.__class__.__name__, self.BASE_CLASS, type(key))
        )

    def __getitem__(self, key):
        if self._check_condition(key):
            if self._default is not None and key not in self:
                dict.__setitem__(self, key, copy(self._default))
            return dict.__getitem__(self, key)
        raise TypeError(
            "%s only accepts keys of type %s, received: %s"
            % (self.__class__.__name__, self.BASE_CLASS, type(key))
        )

    def __setitem__(self, key, value):
        if not self._check_condition(key):
            raise TypeError(
                "%s only accepts keys of type %s, received: %s with value %s"
                % (self.__class__.__name__, self.BASE_CLASS, type(key), value)
            )
        dict.__setitem__(self, key, value)

    @property
    def output_type(self):
        keys_is_list = [isinstance(key, list) for key in self.values()]
        keys_is_list = list(filter(lambda x: x is not False, keys_is_list))
        if len(set(keys_is_list)) == 1:
            return OutputType.MULTIPLE
        return OutputType.SINGLE

    def apply(self, func):
        """Apply a function over values."""
        if not callable(func):
            raise NotACallableError(func)

        obj = copy(self)  # type: ignore
        for key, value in obj.items():
            obj[key] = func(value)
        return obj

    def applymap(self, func):
        """Apply a function over values elementwise."""
        if not callable(func):
            raise NotACallableError(func)

        if self.output_type != OutputType.MULTIPLE:
            raise OutputTypeError(OutputType.MULTIPLE, self.output_type)

        obj = copy(self)
        for key, value in obj.items():
            values = [func(v) for v in value]
            obj[key] = values
        return obj

    def filter(self, func):
        """Filter mapper keys when function returns `True`."""
        if not callable(func):
            raise NotACallableError(func)

        obj = copy(self)  # type: ignore
        for key, value in obj.items():
            if not func(value):
                del obj[key]
        return obj


class EnumDataMapper(DataMapper):
    """Class to map data to Enum."""

    BASE_CLASS = (IntEnum, int)

    def __init__(self, elements, default=None, do_cast=False):
        super(EnumDataMapper, self).__init__(elements, default)
        self.do_cast = do_cast

    def _check_condition(self, key):
        return issubclass(type(key), self.BASE_CLASS)

    def fill_missing_members(self, value):
        """Fill all missing members of the `BASE_CLASS` with `value`."""
        obj = copy(self)  # type: ignore
        for key in self.BASE_CLASS._member_names_:
            if obj.BASE_CLASS[key] not in obj.keys():
                if obj.output_type == OutputType.MULTIPLE and value is not None:
                    _value = [value]
                else:
                    _value = value
                obj[obj.BASE_CLASS[key]] = _value
        return obj

    def sort(self):
        """Sort the mapper with the inner order of its `BASE_CLASS` enum. If multiple enums are present, sorting makes no changes."""
        obj = copy(self)  # type: ignore
        for m in obj.BASE_CLASS._member_names_:
            obj[obj.BASE_CLASS[m]] = obj[obj.BASE_CLASS[m]]
        return obj


class Item(object):
    """A base class to handle a game item backed with enum."""

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


class Attributes(dict):
    """A class to handle attibutes from a EnumDataMapper."""

    def __init__(self, *args, **kwargs):
        super(Attributes, self).__init__(*args, **kwargs)
        self.__dict__ = self

    @classmethod
    def from_nested_dicts(cls, data):
        """Construct nested Attributes from nested dictionaries."""
        if isinstance(data, list):
            return [cls.from_nested_dicts(d) for d in data]

        if issubclass(data.__class__, EnumDataMapper):
            if not data.do_cast:
                return data
            data = dict((key.name.lower(), cls.from_nested_dicts(data[key])) for key in data)
            return cls(data)

        if isinstance(data, dict):
            data = dict((key, cls.from_nested_dicts(data[key])) for key in data)
            return cls(data)

        return data


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


class ScenarioDataMapper(EnumDataMapper):
    """Class to map data to Scenario enum."""

    BASE_CLASS = CoreTypes.Scenario


class ReligionDataMapper(EnumDataMapper):
    """Class to map Religion to Company enum."""

    BASE_CLASS = CoreTypes.Religion


class CompanyDataMapper(EnumDataMapper):
    """Class to map data to Company enum."""

    BASE_CLASS = CoreTypes.Company


class CivDataMapper(EnumDataMapper):
    """Class to map data to Civ enum."""

    BASE_CLASS = CoreTypes.Civ
