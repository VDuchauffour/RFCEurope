import CoreTypes
from copy import copy
from Enum import Enum, IntEnum
from Errors import NotACallableError, OutputTypeError


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


class CompanyDataMapper(EnumDataMapper):
    """Class to map data to Company enum."""

    BASE_CLASS = CoreTypes.Company


class CivDataMapper(EnumDataMapper):
    """Class to map data to Civ enum."""

    BASE_CLASS = CoreTypes.Civ


def sort(iterable, key=lambda x: x, reverse=False):
    return sorted(iterable, key=key, reverse=reverse)
