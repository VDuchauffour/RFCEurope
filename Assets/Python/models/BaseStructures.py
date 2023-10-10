from copy import copy
import random

from Enum import Enum
from Errors import NotACallableError, NotTypeExpectedError, OutputTypeError
from PyUtils import all, any


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

    BASE_CLASS = Enum

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
